import React, { useState, useEffect } from 'react';
import { toast } from "@/components/ui/use-toast";

import Header from '@/components/Header';
import CurrentWeather from '@/components/CurrentWeather';
import WeatherForecast from '@/components/WeatherForecast';
import WeatherDetails from '@/components/WeatherDetails';
import WeatherBackground from '@/components/WeatherBackground';
import { mockWeatherData } from '@/data/mockWeatherData';

// List of available cities
const AVAILABLE_CITIES = [
  "Chennai",
  "Mumbai",
  "Kolkata",
  "Pune"
];

const Index = () => {
  const [weatherData, setWeatherData] = useState(mockWeatherData["Chennai"]);
  const [searchQuery, setSearchQuery] = useState("");
  const [suggestedCities, setSuggestedCities] = useState<string[]>([]);

  useEffect(() => {
    toast({
      title: "Welcome to WeatherVue!",
      description: "View current weather and forecasts for your location.",
      duration: 5000
    });
  }, []);

  const handleSearch = (location: string) => {
    // Update the weather data for the selected city
    const cityData = mockWeatherData[location];
    if (cityData) {
      setWeatherData(cityData);
      toast({
        title: "Location updated",
        description: `Weather data loaded for ${location}`,
        duration: 3000
      });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);

    // Filter cities based on the search query
    const suggestions = AVAILABLE_CITIES.filter(city =>
      city.toLowerCase().includes(query.toLowerCase())
    );
    setSuggestedCities(suggestions);
  };

  const handleSuggestionClick = (city: string) => {
    setSearchQuery(city);
    handleSearch(city);
    setSuggestedCities([]); // Clear suggestions after selection
  };

  return (
    <>
      <WeatherBackground />

      <div className="container mx-auto px-4 py-6 max-w-6xl relative z-10">
        <Header
          onSearch={handleSearch}
          onInputChange={handleInputChange}
          suggestedCities={suggestedCities}
          onSuggestionClick={handleSuggestionClick}
        />


        <>
          <div className="mt-6">
            <CurrentWeather
              location={weatherData.current.location}
              temperature={weatherData.current.temperature}
              condition={weatherData.current.condition}
              high={weatherData.current.high}
              low={weatherData.current.low}
              humidity={weatherData.current.humidity}
              wind={weatherData.current.wind}
              feelsLike={weatherData.current.feelsLike}
            />
          </div>

          <WeatherForecast forecasts={weatherData.forecast} />

          <WeatherDetails
            humidity={weatherData.current.humidity}
            wind={weatherData.current.wind}
            visibility={weatherData.current.visibility}
            pressure={weatherData.current.pressure}
            uvIndex={weatherData.current.uvIndex}
            sunrise={weatherData.current.sunrise}
            sunset={weatherData.current.sunset}
          />
        </>
      </div>
    </>
  );
};

export default Index;
