import React, { useState, useEffect } from 'react';
import ListView from './ListView';

const SearchPage = () => {
    const [region, setRegion] = useState('');
    const [genre, setGenre] = useState('');
    const [results, setResults] = useState([]);
    const [searchType, setSearchType] = useState('cafes');

    // Hardcoded options for filters
    const regionOptions = ['서울', '강남', '홍대', '건대'];
    const genreOptions = ['공포', '추리', 'SF', '어드벤처'];

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
            
            <div className="flex flex-wrap gap-4 mb-4 p-4 border rounded items-center">
                <select value={searchType} onChange={(e) => setSearchType(e.target.value)} className="p-2 border rounded">
                    <option value="cafes">Cafes</option>
                    <option value="themes">Themes</option>
                </select>

                {searchType === 'cafes' ? (
                    <select value={region} onChange={(e) => setRegion(e.target.value)} className="p-2 border rounded">
                        <option value="">All Regions</option>
                        {regionOptions.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                ) : (
                    <select value={genre} onChange={(e) => setGenre(e.target.value)} className="p-2 border rounded">
                        <option value="">All Genres</option>
                        {genreOptions.map(g => <option key={g} value={g}>{g}</option>)}
                    </select>
                )}
                {/* Placeholder for more filters */}
                <div className="p-2 border rounded bg-gray-100 text-gray-500">Difficulty</div>
                <div className="p-2 border rounded bg-gray-100 text-gray-500">Rating</div>
                <div className="p-2 border rounded bg-gray-100 text-gray-500">Players</div>
            </div>

            <div>
                <ListView results={results} type={searchType} />
            </div>
        </div>
    );
};

export default SearchPage;