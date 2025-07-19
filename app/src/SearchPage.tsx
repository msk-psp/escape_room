import React, { useState, useEffect } from 'react';
import ListView from './ListView';
import MapView from './MapView';

const SearchPage = () => {
    const [view, setView] = useState('list'); // 'list' or 'map'
    const [region, setRegion] = useState('');
    const [genre, setGenre] = useState('');
    const [results, setResults] = useState([]);
    const [searchType, setSearchType] = useState('cafes'); // 'cafes' or 'themes'

    useEffect(() => {
        const fetchResults = async () => {
            let url = `http://localhost:8000/${searchType}/?`;
            const params = new URLSearchParams();
            if (searchType === 'cafes' && region) {
                params.append('region', region);
            }
            if (searchType === 'themes' && genre) {
                params.append('name', genre); // Assuming genre maps to theme name
            }
            
            url += params.toString();

            try {
                const response = await fetch(url);
                if (response.ok) {
                    const data = await response.json();
                    setResults(data);
                } else {
                    console.error("Failed to fetch results");
                    setResults([]);
                }
            } catch (error) {
                console.error("Error fetching results:", error);
                setResults([]);
            }
        };

        fetchResults();
    }, [region, genre, searchType]);

    return (
        <div>
            <h1 className="text-3xl font-bold mb-4">Search for Cafes and Themes</h1>
            
            <div className="flex gap-4 mb-4 p-4 border rounded items-center">
                <select value={searchType} onChange={(e) => setSearchType(e.target.value)} className="p-2 border rounded">
                    <option value="cafes">Cafes</option>
                    <option value="themes">Themes</option>
                </select>

                {searchType === 'cafes' ? (
                    <input 
                        type="text" 
                        placeholder="Region (e.g., '서울')" 
                        value={region}
                        onChange={(e) => setRegion(e.target.value)}
                        className="p-2 border rounded"
                    />
                ) : (
                    <input 
                        type="text" 
                        placeholder="Genre (e.g., '공포')" 
                        value={genre}
                        onChange={(e) => setGenre(e.target.value)}
                        className="p-2 border rounded"
                    />
                )}
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
                {view === 'list' ? <ListView results={results} type={searchType} /> : <MapView results={results} />}
            </div>
        </div>
    );
};

export default SearchPage;
