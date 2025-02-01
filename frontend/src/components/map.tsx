"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMap, Circle, useMapEvents } from "react-leaflet";
import { GeoJsonObject, FeatureCollection, Geometry } from "geojson";
import "leaflet/dist/leaflet.css";
import L, { LatLng } from "leaflet";

type GeoJSONData = FeatureCollection<Geometry>;

export class FairPoint { 
  coords: LatLng;
  zone: number;

  constructor(coords: LatLng, zone: number) {
    this.coords = coords;
    this.zone = zone;
  }
};

function FitBounds({ geoData }: { geoData: GeoJsonObject }) {
	const map = useMap();

	useEffect(() => {
		if (!geoData) return;
		const bounds = L.geoJSON(geoData).getBounds();
		map.fitBounds(bounds, { padding: [20, 20] });
		map.setMaxBounds(bounds);
		map.options.maxBoundsViscosity = 1.0;
	}, [geoData, map]);

	return null;
};

function BoundaryCanvas({ geoData }: { geoData: GeoJSONData }) {
  const map = useMap();

  useEffect(() => {
    if (!geoData) return;

    const MaskLayer = L.GridLayer.extend({
      createTile: function (coords: L.Coords) {
        const tile = document.createElement("canvas");
        const size = this.getTileSize();
        tile.width = size.x;
        tile.height = size.y;
        const ctx = tile.getContext("2d");

        if (!ctx) return tile;

        ctx.fillStyle = "#B7B7B7";
        ctx.fillRect(0, 0, size.x, size.y);

        const geoJsonLayer = L.geoJSON(geoData);
        const bounds = geoJsonLayer.getBounds();

        const tileBounds = L.latLngBounds(
          map.unproject([coords.x * size.x, coords.y * size.y], coords.z),
          map.unproject([(coords.x + 1) * size.x, (coords.y + 1) * size.y], coords.z)
        );

        if (bounds.intersects(tileBounds)) {
          ctx.globalCompositeOperation = "destination-out";
          geoJsonLayer.eachLayer((layer) => {
            if (layer instanceof L.Polygon) {
              const latlngs = layer.getLatLngs() as L.LatLng[][];

              ctx.beginPath();
              latlngs[0].forEach((point) => {
                const projected = map.project(point, coords.z);
                ctx.lineTo(projected.x - coords.x * size.x, projected.y - coords.y * size.y);
              });

              ctx.closePath();
              ctx.fill();
            }
          });
        }

        return tile;
      },
    });

    const maskLayer = new MaskLayer();
    maskLayer.addTo(map);

    return () => {
      map.removeLayer(maskLayer);
    };
  }, [geoData, map]);

  return null;
};

interface CoordsProps {
  fairName?: string;
	coords: FairPoint[];
	setCoords: (newCoords: FairPoint[]) => void;
}

function CircleDrawer({ coords, setCoords }: CoordsProps) {
  useMapEvents({
    click(e : L.LeafletMouseEvent) {
			let newCoords = [...coords];
			const tooClose = newCoords.find((point) => {
				const distance = Math.sqrt(
					Math.pow(point.coords.lat - e.latlng.lat, 2) +
					Math.pow(point.coords.lng - e.latlng.lng, 2)
				);
				return distance < 0.0001;
			});
			if (tooClose && window.confirm("Are you sure you want to remove this point?")) {
				newCoords = newCoords.filter(coord => coord !== tooClose);
				setCoords(newCoords);
				return;
			}

			setCoords([...newCoords, new FairPoint(e.latlng, 0)]);
      console.log("Coords", newCoords);
    },
  })

	return null;
}

function getPoints(name: string | undefined): Promise<FairPoint[]> {
  return fetch(`http://192.168.1.85:1488/get_fair_places?fair_name=${name}`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
  }).then((res) => res.json())
    .then((data) => {
      console.log("Data", data);
      return data.map(({ place_cordinates, place_zona } : { place_cordinates: string, place_zona: number }) => {
        console.log("Place", place_cordinates);
        const [lat, lng] = place_cordinates.split(" ").map((coord) => parseFloat(coord));
        return new FairPoint(new LatLng(lat, lng), place_zona);
      });
    })
    .catch((err) => console.error("Error loading points:", err));
}

export default function RevucaMap({ fairName, coords, setCoords }: CoordsProps) {
  const [geoData, setGeoData] = useState<GeoJSONData | null>(null);

  const zoneColors = [
    'blue',
    'red',
    'goldenrod',
    'green',
  ]

  useEffect(() => {
    fetch("/revuca.geo.json")
      .then((res) => res.json())
      .then((data: GeoJSONData) => {
        setGeoData(data);
      })
      .catch((err) => console.error("Error loading GeoJSON:", err));

    getPoints(fairName).then((newCoords: FairPoint[]) => setCoords(newCoords));
  }, []);

  return (
    <MapContainer center={[48.682366, 20.115659]} minZoom={14} maxZoom={18} style={{ height: "500px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {geoData && <GeoJSON data={geoData} style={{ color: "red", fillColor: "transparent" }} />}
      {geoData && <BoundaryCanvas geoData={geoData} />}
      {geoData && <FitBounds geoData={geoData} />}

			{coords && coords?.map((point, index) => {
        console.log(point.zone);
        return (
          <Circle key={index} center={point.coords} radius={4} pathOptions={{color: zoneColors[point.zone]}}/>
        )
      })}

			<CircleDrawer coords={coords} setCoords={setCoords} />
    </MapContainer>
  );
};
