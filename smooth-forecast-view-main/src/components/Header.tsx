import React from 'react';
import { Search, MapPin } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { ThemeToggle } from './ThemeToggle';

interface HeaderProps {
  onSearch: (location: string) => void;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  suggestedCities: string[];
  onSuggestionClick: (city: string) => void;
}

const Header = ({ onSearch, onInputChange, suggestedCities, onSuggestionClick }: HeaderProps) => {
  const [searchValue, setSearchValue] = React.useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchValue.trim()) {
      onSearch(searchValue);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
    onInputChange(e);
  };

  return (
    <header className="py-6 px-4 flex flex-col sm:flex-row justify-between items-center gap-4 animate-fade-in">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl md:text-3xl font-bold text-primary">
          WeatherVue
        </h1>
        <ThemeToggle />
      </div>

      <div className="relative w-full max-w-md">
        <form onSubmit={handleSubmit}>
          <Input
            value={searchValue}
            onChange={handleChange}
            placeholder="Search for a city..."
            className="pl-10 pr-4 py-2 w-full bg-white/70 dark:bg-gray-950/70 backdrop-blur-sm rounded-full border border-gray-200 dark:border-gray-800"
          />
          <button
            type="submit"
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-primary transition-colors"
          >
            <Search size={18} />
          </button>
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
            <MapPin size={18} />
          </div>
        </form>

        {/* Suggested Cities Dropdown */}
        {suggestedCities.length > 0 && (
          <ul className="absolute w-full mt-2 bg-white dark:bg-gray-900 shadow-lg rounded-lg overflow-hidden z-20">
            {suggestedCities.map((city) => (
              <li
                key={city}
                onClick={() => onSuggestionClick(city)}
                className="px-4 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {city}
              </li>
            ))}
          </ul>
        )}
      </div>
    </header>
  );
};

export default Header;
