import { useState } from "react";

import Loader from "../components/Loader";
import PredictionResult from "../components/PredictionResult";

import { predictProtein } from "../services/predictionService";

import {
  predictFastaFile,
  predictFastaText
} from "../services/fastaService";

function Prediction() {

  const [inputText, setInputText] = useState("");
  const [file, setFile] = useState(null);
  const [model, setModel] = useState("esm2_only");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const downloadCSV = () => {

    if (!result?.results) return;

    let csv =
      "Sequence ID,Prediction,Probability\n";

    result.results.forEach((row) => {

      csv +=
        `${row.sequence_id || row.id},${row.prediction},${row.probability}\n`;

    });

    const blob = new Blob(
      [csv],
      {
        type: "text/csv"
      }
    );

    const url =
      URL.createObjectURL(blob);

    const link =
      document.createElement("a");

    link.href = url;

    link.download =
      "prediction_results.csv";

    link.click();
  };

  async function handlePredict() {

    try {

      setLoading(true);

      setError("");

      setResult(null);

      let response;

      if (file) {

        response =
          await predictFastaFile(
            file,
            model
          );

      }

      else if (
        inputText.includes(">")
      ) {

        response =
          await predictFastaText(
            inputText,
            model
          );

      }

      else {

        response =
          await predictProtein(
            inputText,
            model
          );

      }

      setResult(response);

    }

    catch (err) {

      console.error(err);

      setError(
        err?.response?.data?.detail ||
        err?.message ||
        "Prediction failed"
      );

    }

    finally {

      setLoading(false);

    }
  }

  return (

    <div className="prediction-page">

      <div className="prediction-header">

        <h1>
          Parasite Virulence Prediction
        </h1>

        <p>
          Paste a single protein sequence,
          multiple FASTA sequences,
          or upload a FASTA file.
        </p>

      </div>

      <div className="glass-card">

        <label>
          Protein Sequence / FASTA Input
        </label>

        <div
            style={{
                display: "flex",
                gap: "10px",
                marginBottom: "10px"
            }}
        >

            <button
                type="button"
                className="example-btn"
                onClick={() =>
                    setInputText(
`>CAD98656 
MRLSLIIVLLSVIVSAVFSAPAVPLRGTLKDVPVEGSSSSSSSSSSSSSSSSSTSTVAPANKARTGEDAEGSQDSSGTEASGSQGSEEEGSEDDGQTSAASQPTTPAQSEGATTETIEATPKEEFVMWFGEGTPAATLKCGAYTIVYAPIKDQTDPAPRYISGEVTSVTFEKSYNTVKIKVNGQDFSTLSANSSSPTENGGSAGQASSRSRRSLSEETSEAAATVDLFAFTLDGGKRIEVAVPNVEASKRDKYSL
>A0A1A8ZC20
MTISHHQGCGCKEADEVLKGGEFLLKYIDIEKIHGSCRKILKAYDDRLSSDNCESDVDNELIINIPFTNPCKIVSLFLIGGEKGMYPKKMKIFSNREDIDFENINDFKCIQEVELSEDFHGSIEYPLKVYEASPNLADHKIEGAANMTKFSFDAF`)}
            >
                EXAMPLE
            </button>

            <button
                type="button"
                className="clear-btn"
                onClick={() => {

                    setInputText("");
                    setFile(null);
                    setResult(null);
                    setError("");

                }}
            >
                CLEAR INPUT
            </button>

        </div>

        <textarea

          rows="12"

          value={inputText}

          onChange={(e) =>
            setInputText(
              e.target.value
            )
          }

          placeholder={`Single Sequence:

MKTLLVVAAA...

OR

>Protein_1
MKTLLVVAAA

>Protein_2
AAATTTGGG`}

        />

      </div>

      <div className="simple-section">

        <label>
          Upload FASTA File
        </label>

        <input

          type="file"

          accept=".fasta,.fa,.faa"

          onChange={(e) =>
            setFile(
              e.target.files[0]
            )
          }

        />

      </div>

      <div className="simple-section">

        <label>
          Model Combination
        </label>

        <select

          value={model}

          onChange={(e) =>
            setModel(
              e.target.value
            )
          }

        >

          <option value="esm2_only">
            ESM2 Only
          </option>

          <option value="esm2_physchem">
            ESM2 + PhysChem
          </option>

          <option value="prott5_only">
            ProtT5 Only
          </option>

          <option value="prott5_physchem">
            ProtT5 + PhysChem
          </option>

          <option value="esm2_prott5">
            ESM2 + ProtT5
          </option>

          <option value="esm2_prott5_physchem">
            ESM2 + ProtT5 + PhysChem
          </option>

        </select>

      </div>

      <button
        className="predict-btn"
        onClick={handlePredict}
      >
        Predict Virulence
      </button>

      {loading && <Loader />}

      {error && (

        <div className="glass-card">

          <p
            style={{
              color: "#ff6b6b"
            }}
          >
            {error}
          </p>

        </div>

      )}

      {result && (

        <>
          <PredictionResult
            result={result}
          />

          {result?.results && (

            <button
              className="predict-btn"
              onClick={downloadCSV}
            >
              Download CSV
            </button>

          )}

        </>

      )}

    </div>

  );

}

export default Prediction;