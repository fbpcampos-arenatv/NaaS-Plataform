"use client";

import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const geojsonDemonstracao = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { nome: "Zona Crítica" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [-60.03, -3.05],
            [-60.02, -3.05],
            [-60.02, -3.06],
            [-60.03, -3.06],
            [-60.03, -3.05]
          ]
        ]
      }
    }
  ]
};

export default function Mapa() {
  useEffect(() => {
    const mapa = L.map("mapa-naas").setView([-3.05, -60.02], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap"
    }).addTo(mapa);

    L.geoJSON(geojsonDemonstracao, {
      style: {
        color: "#f97316",
        weight: 2,
        fillOpacity: 0.3
      }
    }).addTo(mapa);

    return () => {
      mapa.remove();
    };
  }, []);

  return <div id="mapa-naas" />;
}
