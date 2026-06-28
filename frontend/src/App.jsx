import "./styles/background.css";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AppRoutes from "./routes/AppRoutes";

function App() {

  return (

    <div className="app-background">

      <Navbar />

      <AppRoutes />

      <Footer />

    </div>

  );

}

export default App;