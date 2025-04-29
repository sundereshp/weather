
import React from 'react';
import ForecastCard from './ForecastCard';

interface ForecastData {
  day: string;
  high: number;
  low: number;
  condition: string;
  precipitation: number;
}

const WeatherForecast = ({ forecasts }: { forecasts: ForecastData[] }) => {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">5-Day Forecast</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {forecasts.map((forecast, index) => (
          <ForecastCard
            key={index}
            day={forecast.day}
            high={forecast.high}
            low={forecast.low}
            condition={forecast.condition}
            precipitation={forecast.precipitation}
          />
        ))}
      </div>
    </div>
  );
};

export default WeatherForecast;
