import Dashboard from "./pages/Dashboard";
import NewResearch from "./pages/NewResearch";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ResearchWorkspace from "./pages/ResearchWorkspace";
import ResearchHistory from "./pages/ResearchHistory";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new" element={<NewResearch />} />
        <Route path="/research/:id" element={<ResearchWorkspace />} />
        <Route path="/history" element={<ResearchHistory />} />
      </Routes>
    </BrowserRouter>
  );
}