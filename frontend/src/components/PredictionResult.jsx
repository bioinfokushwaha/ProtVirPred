import ResultsTable from "./ResultsTable";

function PredictionResult({ result }) {
  if (!result) return null;

  const tableData = result.results
    ? result.results
    : [
        {
          sequence_id: "Protein_1",
          prediction: result.prediction,
          probability: result.probability
        }
      ];

  return (
    <div className="glass-card">
      <h2>Prediction Results</h2>
      <ResultsTable results={tableData} />
    </div>
  );
}

export default PredictionResult;