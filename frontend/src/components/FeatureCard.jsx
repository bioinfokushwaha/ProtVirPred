function FeatureCard({
  icon,
  title,
  description,
  onClick
}) {

  return (

    <div
      className="feature-card"
      onClick={onClick}
      style={{
        cursor: "pointer"
      }}
    >

      <div className="feature-icon">
        {icon}
      </div>

      <h3>{title}</h3>

      <p>{description}</p>

    </div>

  );

}

export default FeatureCard;