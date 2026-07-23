{
  description = "Personal semantic retrieval system (notes + embeddings + FAISS)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        python = pkgs.python313;

        pythonEnv = python.withPackages (ps: with ps; [
          # Core runtime
          numpy
	  faiss-cpu
	  sentence-transformers
	  tqdm
        ]);

	numpyCheck = pkgs.runCommand "numoy-check" {} ''
	  set -euo pipefail

	  export PATH=${pythonEnv}/bin:$PATH

          python - << 'EOF'
import numpy as np
print('numpy version:', np.__version__)
assert np.__version__ is not None
EOF
          touch $out
        '';

	faissCheck = pkgs.runCommand "faiss-check" {} ''
          set -euo pipefail

          export PATH=${pythonEnv}/bin:$PATH

          python - << 'EOF'
import faiss
import numpy as np

print("FAISS version check OK")

# dimensionality
d = 16

# create index (L2 distance)
index = faiss.IndexFlatL2(d)

# create some vectors
xb = np.random.random((50, d)).astype('float32')
index.add(xb)

# query vector
xq = np.random.random((1, d)).astype('float32')

D, I = index.search(xq, 5)

print("Distances:", D)
print("Indices:", I)

assert I.shape == (1, 5)
assert D.shape == (1, 5)

print("FAISS retrieval OK")
EOF

  touch $out
'';

          embeddingCheck = pkgs.runCommand "embedding-check" {} ''
            set -euo pipefail

            export PATH=${pythonEnv}/bin:$PATH

            python - << 'EOF'
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "animal rights and ethics",
    "veganism and food choices",
    "quantum physics and particles"
]

embeddings = model.encode(texts)

print("Shape:", embeddings.shape)

assert embeddings.shape[0] == 3
assert embeddings.shape[1] > 0

# sanity: veganism should be closer to animal rights than quantum physics
sim1 = np.dot(embeddings[0], embeddings[1])
sim2 = np.dot(embeddings[0], embeddings[2])

print("sim(0,1):", sim1)
print("sim(0,2):", sim2)

assert sim1 > sim2

print("Embedding sanity OK")
EOF

  touch $out
'';

      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv

            # system tools
            pkgs.git
            pkgs.curl
            pkgs.htop
          ];

          shellHook = ''
            echo "🧠 Personal Semantic Retrieval System Dev Shell"
            echo "Python: $(python --version)"
            echo "FAISS + PyTorch + SQLite ready"
            echo ""
            echo "Next step: python -c 'import faiss; print(\"FAISS OK\")'"
          '';
        };

	checks = {
	  numpy = numpyCheck;
	  faiss = faissCheck;
	  ##embedding = embeddingCheck; not working yet because ddownload will fail
	};

      });
}
