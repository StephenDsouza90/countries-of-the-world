import React, { useEffect, useState } from "react";
import axios from "axios";

const CountriesTable = () => {
  const [countries, setCountries] = useState([]);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState("name"); // Default sort field
  const [orderBy, setOrderBy] = useState("asc"); // Default sort order
  const [limit, setLimit] = useState(null); // Default limit
  const apiUrl = process.env.REACT_APP_API_URL;

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await axios.get(`${apiUrl}/countries`,
          {
            params: {
              limit,
              sortBy,
              orderBy,
            },
          }
        );
        setCountries(response.data.countries);
      } catch (err) {
        setError("Failed to fetch countries. Please try again later.");
      }
    };

    fetchCountries();
  }, [apiUrl, limit, sortBy, orderBy]);

  const handleSortChange = (e) => {
    setSortBy(e.target.value);
  };

  const handleOrderChange = (e) => {
    setOrderBy(e.target.value);
  };

  const handleLimitChange = (e) => {
    setLimit(Number(e.target.value));
  };

  return (
    <div>
      <h1>Countries</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Controls */}
      <div style={{ marginBottom: "1rem" }}>
        <label>
          Sort By: 
          <select value={sortBy} onChange={handleSortChange}>
            <option value="name">Name</option>
            <option value="population">Population</option>
            <option value="area">Area</option>
            <option value="population_density">Population Density</option>
            <option value="region">Region</option>
          </select>
        </label>
        <label style={{ marginLeft: "1rem" }}>
          Order: 
          <select value={orderBy} onChange={handleOrderChange}>
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </label>
        <label style={{ marginLeft: "1rem" }}>
          Limit: 
          <select value={limit} onChange={handleLimitChange}>
            <option value="50">50</option>
            <option value="100">100</option>
            <option value="150">150</option>
            <option value="200">200</option>
            <option value="250">250</option>
          </select>
        </label>
      </div>

      <table border="1" style={{ width: "100%", textAlign: "left" }}>
        <thead>
          <tr>
            <th>#</th>
            <th>Country Name</th>
            <th>Population</th>
            <th>Area</th>
            <th>Population Density</th>
            <th>Region</th>
          </tr>
        </thead>
        <tbody>
          {countries.length > 0 ? (
            countries.map((country, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{country.name}</td>
                <td>{country.population}</td>
                <td>{country.area}</td>
                <td>{country.population_density.toFixed(2)}</td>
                <td>{country.region}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2">No countries available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>      
  );
};

export default CountriesTable;