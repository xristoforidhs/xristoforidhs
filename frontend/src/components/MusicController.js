import React, { useState, useEffect } from "react";
import { Music, Play, Pause, Volume2, Plus, X, Youtube, ExternalLink } from "lucide-react";
import { toast } from "sonner";

export default function MusicController() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentSong, setCurrentSong] = useState(null);
  const [customUrl, setCustomUrl] = useState("");
  const [savedPlaylists, setSavedPlaylists] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    // Load saved playlists from localStorage
    const saved = localStorage.getItem("musicPlaylists");
    if (saved) {
      setSavedPlaylists(JSON.parse(saved));
    }
  }, []);

  const extractVideoId = (url) => {
    // YouTube URL formats
    const youtubeRegex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/;
    const match = url.match(youtubeRegex);
    return match ? match[1] : null;
  };

  const isSpotifyUrl = (url) => {
    return url.includes('spotify.com');
  };

  const addCustomPlaylist = () => {
    if (!customUrl.trim()) {
      toast.error("Please enter a URL");
      return;
    }

    const videoId = extractVideoId(customUrl);
    const isSpotify = isSpotifyUrl(customUrl);

    if (!videoId && !isSpotify) {
      toast.error("Please enter a valid YouTube or Spotify URL");
      return;
    }

    let songName = "Custom Song";
    if (isSpotify) {
      songName = "Spotify Playlist";
    } else {
      songName = `YouTube - ${videoId}`;
    }

    const newSong = {
      id: Date.now(),
      name: songName,
      url: customUrl,
      type: isSpotify ? 'spotify' : 'youtube',
      videoId: videoId
    };

    const updatedPlaylists = [...savedPlaylists, newSong];
    setSavedPlaylists(updatedPlaylists);
    localStorage.setItem("musicPlaylists", JSON.stringify(updatedPlaylists));
    
    setCustomUrl("");
    setShowAddForm(false);
    toast.success("Playlist added!");
  };

  const removePlaylist = (id) => {
    const updatedPlaylists = savedPlaylists.filter(song => song.id !== id);
    setSavedPlaylists(updatedPlaylists);
    localStorage.setItem("musicPlaylists", JSON.stringify(updatedPlaylists));
    toast.success("Playlist removed");
  };

  const playMusic = (song) => {
    stopMusic(); // Stop current music
    
    if (song.type === 'spotify') {
      // Open Spotify in new tab (Spotify doesn't allow embedding)
      window.open(song.url, '_blank');
      toast.info("Spotify opened in new tab!");
      setCurrentSong(song);
      setIsPlaying(true);
    } else {
      // YouTube embed - make it small but visible so audio works
      const iframe = document.createElement('iframe');
      iframe.id = 'music-player';
      iframe.width = '1';
      iframe.height = '1';
      iframe.src = `https://www.youtube.com/embed/${song.videoId}?autoplay=1&loop=1&playlist=${song.videoId}&controls=0&mute=0`;
      iframe.style.position = 'fixed';
      iframe.style.bottom = '0px';
      iframe.style.left = '0px';
      iframe.style.opacity = '0.01';
      iframe.style.pointerEvents = 'none';
      iframe.allow = 'autoplay; encrypted-media';
      document.body.appendChild(iframe);
      
      setCurrentSong(song);
      setIsPlaying(true);
      
      // Try to ensure audio plays
      setTimeout(() => {
        try {
          iframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
        } catch (e) {
          console.log('Could not control iframe');
        }
        toast.success("🎵 Music should be playing now!");
      }, 2000);
    }
  };

  const stopMusic = () => {
    const existingIframe = document.getElementById('music-player');
    if (existingIframe) {
      existingIframe.remove();
    }
    setIsPlaying(false);
    setCurrentSong(null);
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
      padding: '1.5rem',
      zIndex: 1000,
      minWidth: '320px',
      border: '2px solid #e2e8f0'
    }}>
      {/* Header */}
      <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem'}}>
        <Music size={20} />
        <span style={{fontWeight: 600}}>Music Player</span>
        <button
          onClick={stopMusic}
          disabled={!isPlaying}
          style={{
            background: isPlaying ? '#ef4444' : '#e2e8f0',
            color: isPlaying ? 'white' : '#94a3b8',
            border: 'none',
            borderRadius: '50%',
            width: '30px',
            height: '30px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: isPlaying ? 'pointer' : 'not-allowed',
            marginLeft: 'auto'
          }}
        >
          <Pause size={14} />
        </button>
      </div>

      {/* Now Playing */}
      {currentSong && (
        <div style={{
          background: '#f0f9ff',
          padding: '0.75rem',
          borderRadius: '8px',
          marginBottom: '1rem',
          fontSize: '0.875rem',
          color: '#1e40af'
        }}>
          🎵 Playing: {currentSong.name}
          {currentSong.type === 'spotify' && (
            <div style={{fontSize: '0.75rem', marginTop: '0.25rem', color: '#059669'}}>
              📱 Playing in Spotify tab
            </div>
          )}
        </div>
      )}

      {/* Add New Music */}
      <div style={{marginBottom: '1rem'}}>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          style={{
            background: '#22c55e',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            padding: '0.5rem 1rem',
            cursor: 'pointer',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            width: '100%',
            justifyContent: 'center'
          }}
        >
          <Plus size={16} />
          Add YouTube/Spotify URL
        </button>
      </div>

      {/* Add Form */}
      {showAddForm && (
        <div style={{
          background: '#f8fafc',
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '1rem',
          border: '1px solid #e2e8f0'
        }}>
          <div style={{marginBottom: '0.75rem'}}>
            <label style={{fontSize: '0.875rem', color: '#374151', display: 'block', marginBottom: '0.5rem'}}>
              YouTube or Spotify URL:
            </label>
            <input
              type="url"
              placeholder="https://www.youtube.com/watch?v=... or https://open.spotify.com/..."
              value={customUrl}
              onChange={(e) => setCustomUrl(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '4px',
                border: '1px solid #d1d5db',
                fontSize: '0.875rem'
              }}
            />
          </div>
          <div style={{display: 'flex', gap: '0.5rem'}}>
            <button
              onClick={addCustomPlaylist}
              style={{
                background: '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '0.5rem 1rem',
                cursor: 'pointer',
                fontSize: '0.875rem',
                flex: 1
              }}
            >
              Add
            </button>
            <button
              onClick={() => setShowAddForm(false)}
              style={{
                background: '#6b7280',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '0.5rem 1rem',
                cursor: 'pointer',
                fontSize: '0.875rem'
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Saved Playlists */}
      <div>
        <h4 style={{fontSize: '0.875rem', fontWeight: 600, marginBottom: '0.5rem', color: '#374151'}}>
          Your Music ({savedPlaylists.length})
        </h4>
        
        {savedPlaylists.length === 0 ? (
          <p style={{fontSize: '0.875rem', color: '#94a3b8', textAlign: 'center', padding: '1rem'}}>
            No music added yet. Add YouTube or Spotify URLs above.
          </p>
        ) : (
          <div style={{maxHeight: '200px', overflowY: 'auto'}}>
            {savedPlaylists.map(song => (
              <div key={song.id} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.5rem',
                background: currentSong?.id === song.id ? '#dbeafe' : '#f9fafb',
                borderRadius: '6px',
                marginBottom: '0.5rem',
                border: '1px solid #e5e7eb'
              }}>
                <button
                  onClick={() => playMusic(song)}
                  style={{
                    background: '#22c55e',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    width: '24px',
                    height: '24px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer'
                  }}
                >
                  <Play size={12} />
                </button>
                
                <div style={{flex: 1, fontSize: '0.75rem'}}>
                  <div style={{fontWeight: 600, color: '#374151'}}>
                    {song.type === 'spotify' ? '🎵 Spotify' : '▶️ YouTube'}
                  </div>
                  <div style={{color: '#6b7280', fontSize: '0.7rem'}}>
                    {song.name}
                  </div>
                </div>
                
                <button
                  onClick={() => removePlaylist(song.id)}
                  style={{
                    background: '#ef4444',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    width: '20px',
                    height: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer'
                  }}
                >
                  <X size={10} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div style={{
        background: '#fef3c7',
        padding: '0.75rem',
        borderRadius: '6px',
        marginTop: '1rem',
        fontSize: '0.75rem',
        color: '#92400e'
      }}>
        <strong>Tips:</strong><br/>
        • YouTube: Copy any video URL<br/>
        • Spotify: Copy playlist/album URLs<br/>
        • Music plays in background
      </div>
    </div>
  );
}