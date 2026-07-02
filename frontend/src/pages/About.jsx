import "../styles/about.css";

import workflowImage from "../assets/workflow/methodology_workflow.png";

function About() {

  return (

    <div className="about-page">

      <div className="about-title">

        <h1>
          About ParaVirPred
        </h1>

        <p>
          AI-Powered Parasite Virulence Prediction Platform
        </p>

      </div>

      <div className="about-card">

        <section className="about-section">

          <h2>
            🧬 The Biological Mandate & Motivation
          </h2>

          <p>

            Computational approaches to target identification are transforming drug discovery 
            and precision medicine by allowing researchers to identify and prioritise important 
            biological targets from large-scale genomic and proteomic datasets.

            Parasitic diseases caused by protozoan pathogens remain a major challenge for both 
            human health and livestock productivity, causing huge economic losses. Therefore, the 
            development of effective therapeutic and preventive strategies is needed today.

            However, the conventional identification of virulence factors, drug targets, and vaccine 
            candidates largely depends on experimental screening, which is often costly, time-consuming, 
            and resource-intensive.

          </p>

          <p>

            Current subtractive proteomics approaches primarily rely on sequence-similarity-based 
            comparisons with host proteins to identify potential therapeutic targets. While effective 
            in many cases, these methods may overlook functionally important proteins that show limited 
            sequence similarity but maintain conserved structural or biological features.

            To address this limitation, ParaVirPred was developed as an integrated computational platform 
            that combines large protein language models, structural insights, and machine learning 
            techniques for large-scale virulence prediction.

          </p>

          <p>

            Protein language models learn complex evolutionary, structural, and functional patterns 
            from billions of protein sequences and provide deeper representations of protein 
            characteristics beyond conventional sequence-based analyses. ParaVirPred utilises these 
            advanced representations to detect potential virulence-associated proteins with high accuracy, 
            enabling rapid and systematic screening of parasite proteomes. The developed computational 
            framework provides researchers with a powerful tool to accelerate the discovery of novel 
            therapeutic targets and improve our understanding of parasite pathogenic mechanisms.

          </p>

        </section>

        <section className="about-section">

          <h2>
            🖥️ Framework of Protein Language Model and Technical Specifications
          </h2>

          <p>

            The computational architecture of ParaVirPred moves beyond conventional alignment-based 
            approaches by adopting a multimodal machine learning framework that integrates deep 
            biological representations with classical biochemical descriptors.

          </p>

          <ul>

            <li>

              <span className="about-highlight">
                ProtT5-XL-UniRef50
              </span>

              {" "}
              generates 1024-dimensional embeddings capturing
              evolutionary, structural, and functional information
              directly from protein sequences.

            </li>

            <li>

              <span className="about-highlight">
                ESM-2
              </span>

              {" "}
              provides 1280-dimensional transformer-based
              representations that capture residue-level context,
              structural constraints, active sites, and protein
              interaction patterns.

            </li>

            <li>

              <span className="about-highlight">
                Physicochemical Features
              </span>

              {" "}
              complement deep embeddings through biologically
              interpretable descriptors such as molecular weight,
              aromaticity, instability index, isoelectric point,
              GRAVY score, AlphaFold confidence, pocket depth,
              and pocket volume.

            </li>

          </ul>

          <p>

            The integration of language model embeddings and
            physicochemical descriptors enables the system to capture
            both learned biological semantics and experimentally
            interpretable molecular characteristics.

          </p>

        </section>

        <section className="about-section">

          <h2>
            📊 Systematic Benchmarking of Classical Machine Learning and Deep Neural Networks Using Protein Language Model Features for Virulence Prediction
          </h2>

          <p>

            ParaVirPred was developed and systematically evaluated on a carefully curated benchmark 
            dataset comprising approximately 8,928 protein sequences representing both virulent (1288) 
            and non-virulent (7640) proteins. To identify the most effective predictive strategy, 
            a comprehensive comparison of multiple machine learning and deep learning algorithms was 
            performed, including Logistic Regression, Support Vector Machine (SVM), Random Forest, 
            XGBoost, Multi-Layer Perceptron (MLP), Naive Bayes, K-Nearest Neighbours (KNN), and Deep 
            Neural Networks (DNN).

          </p>

          <p>

            A six-feature representation was generated and assessed for predictive performance, 
            including ProtT5 and ESM2 embeddings, physicochemical properties, and their combined 
            hybrid feature spaces. Among the evaluated approaches, the ProtT5 embedding, combined 
            with physicochemical descriptors, consistently yielded the most informative representation 
            for virulence classification. Furthermore, SVM and DNN models showed robust, superior 
            performance across multiple evaluation criteria, including Matthews correlation coefficient 
            (MCC), accuracy, sensitivity, specificity, precision, and F1 Score, demonstrating their 
            effectiveness in reliably identifying virulence-associated proteins.

          </p>

        </section>

        <section className="about-section">

          <h2>
            🗺️ Methodology: Data Processing Workflow
          </h2>

          <p>

            The complete ParaVirPred workflow integrates large-scale
            parasite proteome analysis with deep representation
            learning, machine learning classification, structural
            validation, and downstream target prioritization.

          </p>

          <div className="workflow-container">

            <img
              src={workflowImage}
              alt="Methodology Workflow"
              className="workflow-image"
            />

            <p className="workflow-caption">

              The workflow consists of four major phases:
              input proteome acquisition, multi-modal feature
              engineering, virulence classification using optimized
              machine learning models, and downstream subtractive
              proteomics analyses including host non-homology,
              essentiality assessment, AlphaFold structural validation,
              and binding pocket characterization.

            </p>

          </div>

        </section>

      </div>

    </div>

  );

}

export default About;