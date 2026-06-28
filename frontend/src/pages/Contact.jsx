import "../styles/contact.css";

function Contact() {
  return (
    <div className="contact-page">

      <h1>Contact Us</h1>

      <p className="contact-intro">
        ParaVirPred has been developed at the National Institute of Animal
        Biotechnology (NIAB), Hyderabad. For scientific queries, technical
        support, collaborations, feature requests, or feedback regarding the
        platform, please contact the team.
      </p>

      <div className="contact-container">

        {/* Dr. Sandeep */}

        <div className="contact-card horizontal-card">

          <img
            src="https://avatars.githubusercontent.com/u/37391644?v=4"
            alt="Dr. Sandeep Kushwaha"
            className="contact-image"
          />

          <div className="contact-details">

            <h2>
              <a
                href="https://www.niab.res.in/peoplesandeep/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Dr. Sandeep Kushwaha
              </a>
            </h2>

            <p className="contact-role">
              Scientist-E
            </p>

            <p className="contact-org">
              Molecular Genetics and Bioinformatics Lab
            </p>

            <p className="contact-org">
              National Institute of Animal Biotechnology (NIAB),
              Hyderabad, India - 500032
            </p>

            <p className="contact-org">
              <a
                href="mailto:sandeep@niab.org.in"
                className="contact-email"
              >
                sandeep@niab.org.in
              </a>
            </p>

          </div>

        </div>

        {/* Shekhar */}

        <div className="contact-card horizontal-card">

          <img
            src="https://avatars.githubusercontent.com/u/210685307?v=4"
            alt="Shekhar Gudda"
            className="contact-image"
          />

          <div className="contact-details">

            <h2>
              <a
                href="https://linkedin.com/in/shekhar-gudda-0299062ab"
                target="_blank"
                rel="noopener noreferrer"
              >
                Shekhar Gudda
              </a>
            </h2>

            <p className="contact-role">
              M.Sc. Bioinformatics
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Contact;