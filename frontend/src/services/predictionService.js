import api from "../api/api";

export async function predictProtein(
  sequence,
  combination
) {
  const response = await api.post(
    "/predict",
    {
      sequence,
      combination
    }
  );

  return response.data;
}