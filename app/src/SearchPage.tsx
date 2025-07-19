import React, { useState } from 'react';
import ListView from './ListView';
import MapView from './MapView';

const SearchPage = () => {
    const [view, setView] = useState('list'); // 'list' or 'map'
    const [region, setRegion] = useState('');
    const [genre, setGenre] = useState('');

    const handleSearch = () => {
        // API call logic will go here
        console.log('Searching with filters:', { region, genre });
    };

    return (
        <div>
            <h1 className="text-3xl font-bold mb-4">Search for Cafes and Themes</h1>
            
            <div className="flex gap-4 mb-4 p-4 border rounded">
                <input 
                    type="text" 
                    placeholder="Region (e.g., '서울')" 
                    value={region}
                    onChange={(e) => setRegion(e.target.value)}
                    className="p-2 border rounded"
                />
                <input 
                    type="text" 
                    placeholder="Genre (e.g., '공포')" 
                    value={genre}
                    onChange={(e) => setGenre(e.target.value)}
                    className="p-2 border rounded"
                />
                <button onClick={handleSearch} className="bg-blue-500 text-white p-2 rounded">
                    Search
                </button>
            </div>

            <div className="mb-4">
                <button onClick={() => setView('list')} className={`p-2 ${view === 'list' ? 'bg-gray-300' : ''}`}>
                    List View
                </button>
                <button onClick={() => setView('map')} className={`p-2 ${view === 'map' ? 'bg-gray-300' : ''}`}>
                    Map View
                </button>
            </div>

            <div>
                {view === 'list' ? <ListView /> : <MapView />}
            </div>
        </div>
    );
};

export default SearchPage;