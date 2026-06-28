import niabLogo from "../assets/logos/niab-logo.png";

function Footer() {

  return (

    <footer className="footer">

      <a
        href="https://www.niab.res.in/"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          src={niabLogo}
          alt="NIAB"
          style={{
            width: "80px",
            marginBottom: "10px"
          }}
        />
      </a>
      <p>
        National Institute of Animal Biotechnology (NIAB), Hyderabad, India
      <p>
      </p>
        ParaVirPred © 2026
      </p>

    </footer>

  );

}

export default Footer;