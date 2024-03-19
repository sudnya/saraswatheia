//import * as React from "react";
import React, { useState, useEffect } from 'react';
BASE_URL = 'http://localhost:5001';
BASE_API = '/api/v0';

export default function App() {
  const [token, setToken] = useState(12345);

    getTokenFromBackend(setToken);

    return (
      <p> Hello! {randomNumber} </p>
    );
}

function getTokenFromBackend(setToken) {
  fetch('http://localhost:5001/api/v0/token')
    .then(response => response.json())
    .then(data => {
      setToken(data.token);
    });
}
