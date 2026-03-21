import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

// Temple data structure
interface Temple {
  id: number;
  name: string;
  location: string;
  deity: string;
  significance: string;
  imageUrl: string;
  tags: string[];
}

// Sample temple data
const templesData: Temple[] = [
  {
    id: 1,
    name: "Kamakhya Temple",
    location: "Guwahati, Assam",
    deity: "Goddess Kamakhya",
    significance: "One of the oldest of the 51 Shakti Peethas",
    imageUrl: "https://www.pilgrimagetour.in/blog/wp-content/uploads/2023/12/Travel-Tips-for-to-Visit-Kamakhya-Temple.jpg",
    tags: ["assam", "kamakhya", "tantric", "fertility"]
  },
  {
    id: 2,
    name: "Kalighat Temple",
    location: "Kolkata, West Bengal",
    deity: "Goddess Kali",
    significance: "Where Sati's right toe fell",
    imageUrl: "https://images.unsplash.com/photo-1623677375459-4302b76763c4?auto=format&fit=crop&q=80&w=800",
    tags: ["kolkata", "kali", "bengal", "powerful"]
  },
  {
    id: 3,
    name: "Jwala Ji Temple",
    location: "Kangra, Himachal Pradesh",
    deity: "Goddess Jwalamukhi",
    significance: "Eternal flame represents the goddess",
    imageUrl: "https://images.unsplash.com/photo-1618759287629-ca45d5d7ed1c?auto=format&fit=crop&q=80&w=800",
    tags: ["himachal", "fire", "flame", "jwala"]
  },
  {
    id: 4,
    name: "Vaishno Devi",
    location: "Katra, Jammu & Kashmir",
    deity: "Mata Vaishno Devi",
    significance: "Cave temple with three natural rock formations",
    imageUrl: "https://images.unsplash.com/photo-1624821558130-b325d7946fc4?auto=format&fit=crop&q=80&w=800",
    tags: ["jammu", "kashmir", "cave", "pilgrimage"]
  },
  {
    id: 5,
    name: "Ambaji Temple",
    location: "Banaskantha, Gujarat",
    deity: "Goddess Ambaji",
    significance: "One of the 51 Shakti Peethas where Sati's heart fell",
    imageUrl: "https://images.unsplash.com/photo-1625464264698-fda9e3836efa?auto=format&fit=crop&q=80&w=800",
    tags: ["gujarat", "ambaji", "heart", "powerful"]
  },
  {
    id: 6,
    name: "Dakshineswar Kali Temple",
    location: "Kolkata, West Bengal",
    deity: "Goddess Kali",
    significance: "Associated with Ramakrishna Paramahamsa",
    imageUrl: "https://images.unsplash.com/photo-1623677375459-4302b76763c4?auto=format&fit=crop&q=80&w=800",
    tags: ["kolkata", "kali", "ramakrishna", "spiritual"]
  },
  {
    id: 7,
    name: "Chamundeshwari Temple",
    location: "Mysore, Karnataka",
    deity: "Goddess Chamundeshwari",
    significance: "Presiding deity of Mysore royal family",
    imageUrl: "https://images.unsplash.com/photo-1626160938797-f8b8c4b3b963?auto=format&fit=crop&q=80&w=800",
    tags: ["karnataka", "mysore", "chamundi", "royal"]
  },
  {
    id: 8,
    name: "Maa Chintpurni Temple",
    location: "Una, Himachal Pradesh",
    deity: "Goddess Chintpurni",
    significance: "One of the Shakti Peethas where Sati's feet fell",
    imageUrl: "https://images.unsplash.com/photo-1618759287629-ca45d5d7ed1c?auto=format&fit=crop&q=80&w=800",
    tags: ["himachal", "chintpurni", "feet", "wishes"]
  },
  {
    id: 9,
    name: "Tripura Sundari Temple",
    location: "Udaipur, Tripura",
    deity: "Goddess Tripura Sundari",
    significance: "One of the 51 Shakti Peethas",
    imageUrl: "https://images.unsplash.com/photo-1627307284314-f66486e7b615?auto=format&fit=crop&q=80&w=800",
    tags: ["tripura", "sundari", "powerful", "northeast"]
  },
  {
    id: 10,
    name: "Vindhyavasini Temple",
    location: "Mirzapur, Uttar Pradesh",
    deity: "Goddess Vindhyavasini",
    significance: "Believed to be the manifestation of Durga",
    imageUrl: "https://images.unsplash.com/photo-1625464264698-fda9e3836efa?auto=format&fit=crop&q=80&w=800",
    tags: ["up", "vindhya", "durga", "powerful"]
  }
];

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTemple, setSelectedTemple] = useState<Temple | null>(null);
  const [recommendations, setRecommendations] = useState<Temple[]>([]);

  // Function to calculate similarity score between two temples
  const calculateSimilarity = (temple1: Temple, temple2: Temple) => {
    const tags1 = new Set([...temple1.tags, temple1.location.toLowerCase().split(", ")].flat());
    const tags2 = new Set([...temple2.tags, temple2.location.toLowerCase().split(", ")].flat());
    
    const intersection = new Set([...tags1].filter(x => tags2.has(x)));
    const union = new Set([...tags1, ...tags2]);
    
    return intersection.size / union.size;
  };

  // Function to get temple recommendations
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const getRecommendations = (temple: Temple) => {
    return templesData
      .filter(t => t.id !== temple.id)
      .map(t => ({
        temple: t,
        similarity: calculateSimilarity(temple, t)
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .map(t => t.temple)
      .slice(0, 2);
  };

  // Filter temples based on search query
  const filteredTemples = templesData.filter(temple =>
    temple.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    temple.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
    temple.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  // Update recommendations when a temple is selected
  useEffect(() => {
    if (selectedTemple) {
      setRecommendations(getRecommendations(selectedTemple));
    } else {
      setRecommendations([]);
    }
  }, [getRecommendations, selectedTemple]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-red-800 mb-8">
          Shaktipeeth Temple Guide
        </h1>

        {/* Search Bar */}
        <div className="relative max-w-xl mx-auto mb-12">
          <input
            type="text"
            placeholder="Search temples by name, location, or features..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 pl-12 rounded-lg border border-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
          />
          <Search className="absolute left-4 top-3.5 text-red-400" size={20} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Main Temple List */}
          {!selectedTemple && filteredTemples.map(temple => (
            <div
              key={temple.id}
              onClick={() => setSelectedTemple(temple)}
              className="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer transform transition hover:scale-105"
            >
              <img
                src={temple.imageUrl}
                alt={temple.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h2 className="text-xl font-semibold text-red-800 mb-2">{temple.name}</h2>
                <p className="text-gray-600 mb-2">{temple.location}</p>
                <p className="text-sm text-gray-500">{temple.significance}</p>
              </div>
            </div>
          ))}

          {/* Selected Temple and Recommendations */}
          {selectedTemple && (
            <>
              <div className="lg:col-span-3 mb-8">
                <button
                  onClick={() => setSelectedTemple(null)}
                  className="mb-4 text-red-600 hover:text-red-800"
                >
                  ← Back to all temples
                </button>
                <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                  <img
                    src={selectedTemple.imageUrl}
                    alt={selectedTemple.name}
                    className="w-full h-64 object-cover"
                  />
                  <div className="p-6">
                    <h2 className="text-2xl font-bold text-red-800 mb-3">
                      {selectedTemple.name}
                    </h2>
                    <p className="text-gray-600 mb-2">{selectedTemple.location}</p>
                    <p className="text-gray-700 mb-4">{selectedTemple.significance}</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedTemple.tags.map(tag => (
                        <span
                          key={tag}
                          className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              {recommendations.length > 0 && (
                <div className="lg:col-span-3">
                  <h3 className="text-xl font-semibold text-red-800 mb-4">
                    Similar Temples You May Like
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {recommendations.map(temple => (
                      <div
                        key={temple.id}
                        onClick={() => setSelectedTemple(temple)}
                        className="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer transform transition hover:scale-105"
                      >
                        <img
                          src={temple.imageUrl}
                          alt={temple.name}
                          className="w-full h-48 object-cover"
                        />
                        <div className="p-4">
                          <h2 className="text-xl font-semibold text-red-800 mb-2">
                            {temple.name}
                          </h2>
                          <p className="text-gray-600 mb-2">{temple.location}</p>
                          <p className="text-sm text-gray-500">{temple.significance}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;