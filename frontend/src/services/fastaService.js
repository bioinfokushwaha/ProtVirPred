import api from "../api/api";

export const predictFastaFile = async (
  file,
  modelName
) => {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  formData.append(
    "model_name",
    modelName
  );

  const response =
    await api.post(
      "/predict-fasta-file",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data"
        }
      }
    );

  return response.data;
};

export const predictFastaText = async (
  fastaText,
  modelName
) => {

  const response =
    await api.post(
      "/predict-fasta",
      {
        fasta: fastaText,
        combination: modelName
      }
    );

  return response.data;
};