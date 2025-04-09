import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const CountryDetailsPage = () => {
  const { countryName } = useParams();
  const navigate = useNavigate();

  const [countryInfo, setCountryInfo] = useState(null);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState({
    info: false,
    images: false,
    upload: false,
  });
  const [error, setError] = useState({
    info: null,
    images: null,
    upload: null,
  });

  const [newImage, setNewImage] = useState(null);
  const [newImageTitle, setNewImageTitle] = useState('');
  const [newImageDescription, setNewImageDescription] = useState('');

  let apiUrl = process.env.REACT_APP_API_URL;
  console.log("API URL:", apiUrl);

  // If apiUrl is not set, hard code it for testing
  if (!apiUrl) {
    console.warn("API URL is not set. Using hardcoded URL for testing.");
    apiUrl = "http://localhost:8080"; // Replace with your actual API URL
  }

  console.log("API URL:", apiUrl);

  // Fetch country info
  useEffect(() => {
    const fetchCountryInfo = async () => {
      setLoading((prev) => ({ ...prev, info: true }));
      setError((prev) => ({ ...prev, info: null }));

      try {
        const response = await axios.get(`${apiUrl}/countries/${countryName}`);
        setCountryInfo(response.data);
      } catch (err) {
        setError((prev) => ({ ...prev, info: 'Failed to fetch country information' }));
        console.error('Error fetching country information:', err);
      } finally {
        setLoading((prev) => ({ ...prev, info: false }));
      }
    };

    fetchCountryInfo();
  }, [apiUrl, countryName]);

  // Fetch country images
  useEffect(() => {
    const fetchCountryImages = async () => {
      setLoading((prev) => ({ ...prev, images: true }));
      setError((prev) => ({ ...prev, images: null }));

      try {
        const response = await axios.get(`${apiUrl}/countries/${countryName}/images`);
        setImages(response.data.images || []);
      } catch (err) {
        setError((prev) => ({ ...prev, images: 'Failed to fetch country images' }));
        console.error('Error fetching country images:', err);
      } finally {
        setLoading((prev) => ({ ...prev, images: false }));
      }
    };

    fetchCountryImages();
  }, [apiUrl, countryName]);

  // Handle image upload
  const handleImageUpload = async (e) => {
    e.preventDefault();
    if (!newImage || !newImageTitle || !newImageDescription) {
      setError((prev) => ({ ...prev, upload: 'Please provide an image, title, and description.' }));
      return;
    }

    const formData = new FormData();
    formData.append('file', newImage);
    formData.append('title', newImageTitle);
    formData.append('description', newImageDescription);

    try {
      setLoading((prev) => ({ ...prev, upload: true }));
      setError((prev) => ({ ...prev, upload: null }));

      await axios.post(`${apiUrl}/countries/${countryName}/images`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Refresh images after upload
      const response = await axios.get(`${apiUrl}/countries/${countryName}/images`);
      setImages(response.data.images || []);
      setNewImage(null);
      setNewImageTitle('');
      setNewImageDescription('');
    } catch (err) {
      setError((prev) => ({ ...prev, upload: 'Failed to upload image' }));
      console.error('Error uploading image:', err);
    } finally {
      setLoading((prev) => ({ ...prev, upload: false }));
    }
  };

  return (
    <div className="country-details-page">
      <button onClick={() => navigate(-1)} style={{ marginBottom: '20px' }}>
        ← Back to Countries
      </button>

      <h1>{countryName}</h1>

      {/* Country Info Section */}
      {loading.info ? (
        <div>Loading country information...</div>
      ) : error.info ? (
        <div className="error-message">{error.info}</div>
      ) : countryInfo ? (
        <div className="country-info">
          <h2>Country Information</h2>
          <table border="1" style={{ width: '100%', textAlign: 'left' }}>
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
              <tr>
                <td>1</td>
                <td>{countryInfo.country.country_name}</td>
                <td>{countryInfo.country.population || 'N/A'}</td>
                <td>{countryInfo.country.area || 'N/A'}</td>
                <td>
                  {countryInfo.country.population && countryInfo.country.area
                    ? (countryInfo.country.population / countryInfo.country.area).toFixed(2)
                    : 'N/A'}
                </td>
                <td>{countryInfo.country.region || 'N/A'}</td>
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div>No information available for {countryName}</div>
      )}

      {/* Image Upload Section */}
      <div className="image-upload">
        <h2>Upload an Image</h2>
        {error.upload && <div className="error-message">{error.upload}</div>}
        <form onSubmit={handleImageUpload}>
          <div>
            <label>
              Image:
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setNewImage(e.target.files[0])}
              />
            </label>
          </div>
          <div>
            <label>
              Title:
              <input
                type="text"
                value={newImageTitle}
                onChange={(e) => setNewImageTitle(e.target.value)}
                placeholder="Enter image title"
              />
            </label>
          </div>
          <div>
            <label>
              Description:
              <textarea
                value={newImageDescription}
                onChange={(e) => setNewImageDescription(e.target.value)}
                placeholder="Enter image description"
              />
            </label>
          </div>
          <button type="submit" disabled={loading.upload}>
            {loading.upload ? 'Uploading...' : 'Upload'}
          </button>
        </form>
      </div>

      {/* Country Images Section */}
      <div className="country-images">
        <h2>Images</h2>
        {loading.images ? (
          <div>Loading images...</div>
        ) : error.images ? (
          <div className="error-message">{error.images}</div>
        ) : images.length > 0 ? (
          <div className="image-gallery" style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
            {images.map((image, index) => (
              <div key={index} style={{ textAlign: 'center' }}>
                <img
                  src={`data:image/jpeg;base64,${image.file}`} // Add the prefix here
                  alt={image.title || `${countryName} ${index + 1}`}
                  style={{ maxWidth: '200px', maxHeight: '200px' }}
                />
                <h4>{image.title || 'Untitled'}</h4>
                <p>{image.description || 'No description available'}</p>
              </div>
            ))}
          </div>
        ) : (
          <div>No images available for {countryName}</div>
        )}
      </div>
    </div>
  );
};

export default CountryDetailsPage;