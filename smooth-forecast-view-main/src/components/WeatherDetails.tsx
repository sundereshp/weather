
import React from 'react';
import { Card } from '@/components/ui/card';
import { Umbrella, Wind, Droplet, Sun, Cloud } from 'lucide-react';

interface WeatherDetailsProps {
  humidity: number;
  wind: number;
  visibility: number;
  pressure: number;
  uvIndex: number;
  sunrise: string;
  sunset: string;
}


const WeatherDetails = ({
  humidity,
  wind,
  visibility,
  pressure,
  uvIndex,
  sunrise,
  sunset,
}: WeatherDetailsProps) => {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Today's Details</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="p-5 bg-gradient-to-r from-white/80 to-weather-lightBlue/20 backdrop-blur-sm border-white/30 animate-fade-in">
          <h3 className="text-lg font-medium mb-4 flex items-center">
            <Umbrella size={20} className="mr-2 text-primary" />
            Air Conditions
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Humidity</p>
              <p className="text-xl font-semibold">{humidity}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Wind</p>
              <p className="text-xl font-semibold">{wind} mph</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Visibility</p>
              <p className="text-xl font-semibold">{visibility} miles</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Pressure</p>
              <p className="text-xl font-semibold">{pressure} hPa</p>
            </div>
          </div>
        </Card>
        
        <Card className="p-5 bg-gradient-to-r from-white/80 to-weather-warm/20 backdrop-blur-sm border-white/30 animate-fade-in">
          <h3 className="text-lg font-medium mb-4 flex items-center">
            <Sun size={20} className="mr-2 text-yellow-500" />
            Sun & UV
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">UV Index</p>
              <p className="text-xl font-semibold">{uvIndex}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Sunrise</p>
              <p className="text-xl font-semibold">{sunrise}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Sunset</p>
              <p className="text-xl font-semibold">{sunset}</p>
            </div>
            <div className="flex items-center justify-start">
              <Cloud size={24} className="text-weather-blue animate-pulse-slow" />
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default WeatherDetails;
