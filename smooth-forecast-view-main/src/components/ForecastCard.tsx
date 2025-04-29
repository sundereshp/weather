
import React from 'react';
import { Cloud, CloudRain, CloudSnow, Sun } from 'lucide-react';

interface ForecastCardProps {
  day: string;
  high: number;
  low: number;
  condition: string;
  precipitation: number;
}

const ForecastCard = ({ day, high, low, condition, precipitation }: ForecastCardProps) => {
  const getWeatherIcon = () => {
    switch (condition.toLowerCase()) {
      case 'rain':
        return <CloudRain className="w-10 h-10 text-weather-blue" />;
      case 'snow':
        return <CloudSnow className="w-10 h-10 text-weather-blue" />;
      case 'sunny':
        return <Sun className="w-10 h-10 text-yellow-500" />;
      case 'cloudy':
      default:
        return <Cloud className="w-10 h-10 text-weather-blue" />;
    }
  };

  return (
    <div className="weather-card p-4 flex flex-col items-center animate-fade-in">
      <p className="font-medium text-gray-700">{day}</p>
      <div className="my-3">{getWeatherIcon()}</div>
      <p className="text-sm text-gray-500">{condition}</p>
      <div className="mt-2 flex justify-between w-full">
        <p className="text-gray-800 font-medium">{high}°</p>
        <p className="text-gray-500">{low}°</p>
      </div>
      <div className="mt-2 text-xs text-gray-500">
        {precipitation > 0 ? `${precipitation}% rain` : 'No rain'}
      </div>
    </div>
  );
};

export default ForecastCard;
