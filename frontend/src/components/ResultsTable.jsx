function ResultsTable({ results }) {

  if (!results || results.length === 0)
    return null;

  return (

    <table className="results-table">

      <thead>

        <tr>

          <th>Sr.No.</th>

          <th>Sequence ID</th>

          <th>Prediction</th>

          <th>Probability</th>

        </tr>

      </thead>

      <tbody>

        {results.map((row, index) => (

          <tr key={index}>

            <td>{index + 1}</td>

            <td>
              {row.sequence_id || row.id}
            </td>

            <td
              className={
                row.prediction
                  ?.toLowerCase()
                  .includes("non")
                  ? "nonvirulent-text"
                  : "virulent-text"
              }
            >
              {row.prediction}
            </td>

            <td>
              {(
                Number(row.probability) * 100
              ).toFixed(2)}%
            </td>

          </tr>

        ))}

      </tbody>

    </table>

  );

}

export default ResultsTable;