import React from "react";
import { Routes, Route } from "react-router-dom";
import CountriesTable from "./components/CountriesTable";
import CountryDetailsPage from "./components/CountryDetailsPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<CountriesTable />} />
      <Route path="/countries/:countryName" element={<CountryDetailsPage />} />
      <Route path="/health" element={<div>OK</div>} />
    </Routes>
  );
}

export default App;