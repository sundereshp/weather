import React, { useState, useEffect } from 'react';
import { toast } from "@/components/ui/use-toast";

import Header from '@/components/Header';
import CurrentWeather from '@/components/CurrentWeather';
import WeatherForecast from '@/components/WeatherForecast';
import WeatherDetails from '@/components/WeatherDetails';
import WeatherBackground from '@/components/WeatherBackground';

const AVAILABLE_CITIES = [
  "Chennai",
  "Mumbai",
  "Kolkata",
  "Pune"
];

const Index = () => {
  const [weatherData, setWeatherData] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [suggestedCities, setSuggestedCities] = useState<string[]>([]);

  useEffect(() => {
    toast({
      title: "Welcome to WeatherVue!",
      description: "View current weather and forecasts for your location.",
      duration: 5000
    });

    // Load default city
    handleSearch("Chennai");
  }, []);

  const handleSearch = async (location: string) => {
    try {
      const response = await fetch(`http://localhost:5000/search?city=${location}`);
      const data = await response.json();

      if (response.ok) {
        setWeatherData(data);
        toast({
          title: "Weather Loaded",
          description: `Weather data loaded for ${location}`,
          duration: 3000
        });
      } else {
        toast({
          title: "Error",
          description: data.error || "Failed to fetch weather",
          duration: 3000,
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Network Error",
        description: "Could not connect to the weather server.",
        duration: 3000,
        variant: "destructive"
      });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);

    const suggestions = AVAILABLE_CITIES.filter(city =>
      city.toLowerCase().includes(query.toLowerCase())
    );
    setSuggestedCities(suggestions);
  };

  const handleSuggestionClick = (city: string) => {
    setSearchQuery(city);
    setSuggestedCities([]);
    handleSearch(city);
  };

  return (
    <>
      <WeatherBackground />

      <div className="container mx-auto px-4 py-6 max-w-6xl relative z-10">
        <Header
          suggestedCities={suggestedCities}
          onSuggestionClick={handleSuggestionClick}
          setWeatherData={setWeatherData}
        />

        <div className="mt-6">
          {weatherData && weatherData.forecast && (
            <>
              <CurrentWeather
                location={weatherData.city_name}
                temperature={weatherData.temperature}
                condition={weatherData.condition_description}
                high={weatherData.temperature + 2}
                low={weatherData.temperature - 2}
                humidity={weatherData.humidity}
                wind={weatherData.wind_speed}
                feelsLike={weatherData.feels_like}
              />

              <WeatherDetails
                humidity={weatherData.humidity}
                wind={weatherData.wind_speed}
                visibility={weatherData.visibility}
                pressure={weatherData.pressure}
                uvIndex={weatherData.uvIndex}
                sunrise={weatherData.sunrise}
                sunset={weatherData.sunset}
              />

              <WeatherForecast forecasts={weatherData.forecast} />
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default Index;
