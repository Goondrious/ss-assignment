import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Image from "./pages/Image";
import "./App.css";

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/image/:imageId" element={<Image />} />
      </Routes>
    </>
  );
};

export default App;
