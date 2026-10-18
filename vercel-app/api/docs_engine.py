"""
Lightweight BM25 Documentation Memory & Search for Vercel Serverless.
Indexes docs/ directory in memory on function cold start.
"""

import os
import re
import math
from typing import List, Dict, Any, Optional

class ServerlessDocsMemory:
    def __init__(self, docs_path: str = "docs"):
        self.docs_root = os.path.realpath(docs_path)
        self.docs: List[Dict[str, Any]] = []
        self.inverted_index: Dict[str, Dict[int, float]] = {}
        self.df: Dict[str, int] = {}
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        
        self.synonyms: Dict[str, List[str]] = {
            "postgres": ["postgresql", "pg", "wal2json", "pgoutput"],
            "mongo": ["mongodb", "oplog", "replica"],
            "oracle": ["logminer", "cdc", "archivelog"],
            "iceberg": ["rest", "glue", "jdbc", "hive", "catalog", "lakehouse"],
            "kafka": ["source", "offset", "topic"],
            "docker": ["compose", "container", "ui"],
            "k8s": ["kubernetes", "helm", "chart"],
            "cdc": ["change data capture", "replication", "binlog"]
        }
        
        # Semantic concept mapping for ambiguous / non-literal queries
        self.semantic_concepts: Dict[str, List[str]] = {
            "mask": ["normalization", "filter", "stream", "columns"],
            "pii": ["normalization", "filter", "selected_streams", "columns"],
            "lag": ["cdc", "wal", "replication", "tuning", "performance", "delay"],
            "slow": ["cdc", "benchmarks", "performance", "tuning", "worker"],
            "stuck": ["troubleshooting", "job", "worker", "status", "replication"],
            "stopped": ["troubleshooting", "error", "checkpoint", "state"],
            "chart": ["bi", "trino", "superset", "metabase", "duckdb"],
            "dbt": ["airflow", "orchestration", "dagster", "downstream"],
            "delete": ["read-only", "never", "source", "replication_slot"],
            "iam": ["aws", "role", "credentials", "s3", "glue", "policy"]
        }
        self.load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'[a-zA-Z0-9_\-\.]+', text.lower())
        return [t for t in tokens if len(t) > 1]

    def load_and_index(self):
        self.docs = []
        self.inverted_index = {}
        self.df = {}
        self.doc_lengths = []

        doc_idx = 0
        for root, _, files in os.walk(self.docs_root):
            for file in sorted(files):
                if file.endswith((".md", ".mdx")):
                    full_path = os.path.realpath(os.path.join(root, file))
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(self.docs_root))
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        # Extract title
                        title = os.path.splitext(file)[0].replace("-", " ").title()
                        for line in content.splitlines()[:15]:
                            if line.startswith("# ") or line.startswith("title:"):
                                title = line.replace("#", "").replace("title:", "").strip().strip('"\'')
                                break

                        tokens = self._tokenize(content)
                        doc_len = len(tokens)
                        self.doc_lengths.append(doc_len)

                        tf: Dict[str, float] = {}
                        for t in tokens:
                            tf[t] = tf.get(t, 0) + 1

                        for term, freq in tf.items():
                            if term not in self.inverted_index:
                                self.inverted_index[term] = {}
                                self.df[term] = 0
                            self.inverted_index[term][doc_idx] = freq
                            self.df[term] += 1

                        snippet = re.sub(r'(\n|#|\*|`|\[|\]|\(.*?\)|\<.*?\>)', ' ', content[:300]).strip()
                        self.docs.append({
                            "id": doc_idx,
                            "path": rel_path,
                            "full_path": full_path,
                            "title": title,
                            "content": content,
                            "snippet": snippet[:180]
                        })
                        doc_idx += 1
                    except Exception:
                        pass

        if self.doc_lengths:
            self.avg_doc_len = sum(self.doc_lengths) / len(self.doc_lengths)

    def search_docs(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        tokens = self._tokenize(query)
        if not tokens or not self.docs:
            return []

        expanded = set(tokens)
        for t in tokens:
            if t in self.synonyms:
                expanded.update(self.synonyms[t])
            if t in self.semantic_concepts:
                expanded.update(self.semantic_concepts[t])

        N = len(self.docs)
        k1 = 1.2
        b = 0.75
        scores: Dict[int, float] = {}

        for term in expanded:
            if term not in self.inverted_index:
                continue
            df_val = self.df.get(term, 0)
            idf = math.log(1.0 + (N - df_val + 0.5) / (df_val + 0.5))
            for doc_idx, freq in self.inverted_index[term].items():
                doc_len = self.doc_lengths[doc_idx]
                tf_norm = (freq * (k1 + 1.0)) / (freq + k1 * (1.0 - b + b * (doc_len / (self.avg_doc_len or 1.0))))
                score = idf * tf_norm
                
                # Semantic Title Boost (3x weight if term matches title)
                doc_title = self.docs[doc_idx]["title"].lower()
                if term in doc_title:
                    score *= 3.0
                    
                scores[doc_idx] = scores.get(doc_idx, 0.0) + score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_idx, score in ranked[:limit]:
            d = self.docs[doc_idx]
            results.append({
                "path": d["path"],
                "title": d["title"],
                "content": d["content"],
                "snippet": d["snippet"],
                "score": score
            })
        return results

