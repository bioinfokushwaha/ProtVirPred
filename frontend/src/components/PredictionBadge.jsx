function PredictionBadge({
  prediction
}) {

  const virulent =
    prediction === "Virulent";

  return (

    <div
      className={
        virulent
          ? "badge-virulent"
          : "badge-safe"
      }
    >
      {prediction}
    </div>

  );
}

export default PredictionBadge;