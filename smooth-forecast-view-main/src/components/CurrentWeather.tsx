
import React from 'react';
import { Cloud, Droplet, Wind, Thermometer } from 'lucide-react';
import { Card } from '@/components/ui/card';

interface CurrentWeatherProps {
  location: string;
  temperature: number;
  condition: string;
  high: number;
  low: number;
  humidity: number;
  wind: number;
  feelsLike: number;
}

const CurrentWeather = ({
  location,
  temperature,
  condition,
  high,
  low,
  humidity,
  wind,
  feelsLike
}: CurrentWeatherProps) => {
  return (
    <Card className="w-full overflow-hidden backdrop-blur-lg bg-gradient-to-r from-weather-blue/10 to-weather-lightBlue/30 border-white/20 shadow-lg rounded-2xl animate-fade-in">
      <div className="p-6 md:p-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="text-center md:text-left">
            <h2 className="text-xl sm:text-2xl font-medium text-gray-700">{location}</h2>
            <p className="text-sm text-gray-500 mt-1">Today, {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</p>
            
            <div className="mt-4 flex items-center justify-center md:justify-start">
              <Cloud className="text-weather-blue h-16 w-16 md:h-20 md:w-20 mr-2" />
              <div>
                <div className="text-5xl md:text-6xl font-bold text-gray-800">{temperature}°</div>
                <p className="text-gray-600">{condition}</p>
              </div>
            </div>
            
            <div className="mt-3 flex items-center justify-center md:justify-start">
              <p className="text-gray-700 font-medium">H: {high}° L: {low}°</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4 sm:gap-6 w-full md:w-auto">
            <div className="weather-glass p-3 sm:p-4 rounded-xl flex items-center">
              <Thermometer size={20} className="text-primary mr-3" />
              <div>
                <p className="text-xs text-gray-500">Feels Like</p>
                <p className="text-lg font-semibold">{feelsLike}°</p>
              </div>
            </div>
            
            <div className="weather-glass p-3 sm:p-4 rounded-xl flex items-center">
              <Droplet size={20} className="text-primary mr-3" />
              <div>
                <p className="text-xs text-gray-500">Humidity</p>
                <p className="text-lg font-semibold">{humidity}%</p>
              </div>
            </div>
            
            <div className="weather-glass p-3 sm:p-4 rounded-xl flex items-center">
              <Wind size={20} className="text-primary mr-3" />
              <div>
                <p className="text-xs text-gray-500">Wind</p>
                <p className="text-lg font-semibold">{wind} mph</p>
              </div>
            </div>
            
            <div className="weather-glass p-3 sm:p-4 rounded-xl flex items-center">
              <Cloud size={20} className="text-primary mr-3" />
              <div>
                <p className="text-xs text-gray-500">Condition</p>
                <p className="text-lg font-semibold truncate max-w-[80px]">{condition}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default CurrentWeather;
