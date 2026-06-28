import "../styles/download.css";

function Download() {

  const API =
      import.meta.env.VITE_API_BASE_URL || "";

  return (

    <div className="download-page">

      <div className="download-header">

        <h1>
          Downloads
        </h1>

        <p>
          Download pre-trained models,
          benchmark datasets and standalone
          prediction tools for offline
          parasite virulence prediction.
        </p>

      </div>

      {/* Models */}

      <div className="glass-card">

        <h2>
          Pre-trained Models
        </h2>

        <table className="download-table">

          <thead>

            <tr>

              <th>Feature Space</th>

              <th>Best Model</th>

              <th>Download</th>

            </tr>

          </thead>

          <tbody>

            <tr>

              <td>ESM2 Only</td>

              <td>DNN</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/esm2_only_dnn.pth`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

            <tr>

              <td>ProtT5 Only</td>

              <td>SVM</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/prott5_only_svm.pkl`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

            <tr>

              <td>ESM2 + PhysChem</td>

              <td>XGBoost</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/esm2_physchem_xgb.pkl`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

            <tr>

              <td>ProtT5 + PhysChem</td>

              <td>DNN</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/prott5_physchem_dnn.pth`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

            <tr>

              <td>ESM2 + ProtT5</td>

              <td>SVM</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/esm2_prott5_svm.pkl`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

            <tr>

              <td>ESM2 + ProtT5 + PhysChem</td>

              <td>DNN</td>

              <td>

                <button
                  onClick={() =>
                    window.open(
                      `${API}/download-model/esm2_prott5_physchem_dnn.pth`
                    )
                  }
                >
                  Download
                </button>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

      {/* Dataset */}

      <div className="glass-card">

        <h2>
          Benchmark Dataset
        </h2>

        <p>

          Includes training dataset,
          independent validation dataset
          and README documentation.

        </p>

        <button
          className="download-btn"
          onClick={() =>
            window.open(
              `${API}/download-dataset`
            )
          }
        >
          Download Dataset
        </button>

      </div>

      {/* Script */}

      <div className="glass-card">

        <h2>
          Standalone Python Pipeline
        </h2>

        <p>

          Download the standalone
          prediction pipeline for
          local virulence prediction.

        </p>

        <button
          className="download-btn"
          onClick={() =>
            window.open(
              `${API}/download-script`
            )
          }
        >
          Download predict_virulence.py
        </button>

      </div>

      {/* Offline Usage Instructions */}

      <div className="glass-card">

        <h2>
          Offline Usage Instructions
        </h2>

        <p>
          ParaVirPred can be executed locally using the downloaded
          prediction script and pre-trained models. Follow the
          instructions below:
        </p>

        <ol className="download-instructions">

          <li>
            Download the required pre-trained model from the table above.
          </li>

          <li>
            Download the standalone prediction script
            <strong> predict_virulence.py </strong>.
          </li>

          <li>
            Create a working directory and place the downloaded model
            and prediction script inside the same folder.
          </li>

          <li>
            Install the required Python packages:
            <pre>
pip install torch transformers esm biopython numpy pandas scikit-learn xgboost joblib tqdm
            </pre>
          </li>

          <li>
            Prepare your protein sequences in FASTA format.
          </li>

          <li>
            Run prediction:
            <pre>
python predict_virulence.py --input proteins.fasta --model model_file
            </pre>
          </li>

          <li>
            The generated CSV file will contain:
            <ul>
              <li>Protein ID</li>
              <li>Prediction (Virulent / Non-Virulent)</li>
              <li>Probability Score</li>
            </ul>
          </li>

          <li>
            For large-scale prediction (&gt;1000 proteins), we recommend
            running the standalone version locally using a workstation
            equipped with a dedicated GPU.
          </li>

        </ol>

      </div>

    </div>

  );

}

export default Download;