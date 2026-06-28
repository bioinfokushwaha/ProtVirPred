import { useState } from "react";

function FASTAUpload({
  file,
  setFile
}) {

  const handleChange = (e) => {

    const selectedFile =
      e.target.files[0];

    if (selectedFile) {

      setFile(
        selectedFile
      );
    }
  };

  return (

    <div>

      <input
        type="file"
        accept=".fasta,.fa,.faa,.txt"
        onChange={
          handleChange
        }
      />

      {file && (

        <p>
          Selected:
          {" "}
          {file.name}
        </p>

      )}

    </div>
  );
}

export default FASTAUpload;