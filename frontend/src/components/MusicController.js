import React, { useState } from "react";
import { Music, Play, Pause, Volume2 } from "lucide-react";

export default function MusicController() {
  const [currentSong, setCurrentSong] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.3);
  const [audioElement, setAudioElement] = useState(null);

  const musicOptions = [
    {
      id: 'christmas-1',
      name: 'Jingle Bells Classic',
      url: 'https://www.soundjay.com/misc/sounds/jingle_bells.mp3',
      youtube: 'https://www.youtube.com/embed/3Uo0JAUWijM?autoplay=1&loop=1&playlist=3Uo0JAUWijM'
    },
    {
      id: 'christmas-2', 
      name: 'Christmas Piano',
      url: 'https://www.soundjay.com/misc/sounds/christmas_piano.mp3',
      youtube: 'https://www.youtube.com/embed/VbBb0zLJ5wg?autoplay=1&loop=1&playlist=VbBb0zLJ5wg'
    },
    {
      id: 'relaxing-1',
      name: 'Relaxing Background',
      url: 'https://www.soundjay.com/misc/sounds/relaxing.mp3',
      youtube: 'https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1&loop=1&playlist=jfKfPfyJRdk'
    },
    {
      id: 'upbeat-1',
      name: 'Upbeat Shopping',
      url: 'https://www.soundjay.com/misc/sounds/upbeat.mp3',
      youtube: 'https://www.youtube.com/embed/ZbZSe6N_BXs?autoplay=1&loop=1&playlist=ZbZSe6N_BXs'
    }
  ];

  const playMusic = (song) => {
    // Stop current music
    stopMusic();
    
    // Create YouTube iframe for background music
    const iframe = document.createElement('iframe');
    iframe.id = 'music-player';
    iframe.width = '0';
    iframe.height = '0';
    iframe.src = song.youtube + '&controls=0';
    iframe.style.display = 'none';
    iframe.allow = 'autoplay; encrypted-media';
    document.body.appendChild(iframe);
    
    setCurrentSong(song);
    setIsPlaying(true);
  };

  const stopMusic = () => {
    const existingIframe = document.getElementById('music-player');
    if (existingIframe) {
      existingIframe.remove();
    }
    setIsPlaying(false);
    setCurrentSong(null);
  };

  const togglePlayPause = () => {
    if (isPlaying) {
      stopMusic();
    } else if (currentSong) {
      playMusic(currentSong);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
      padding: '1rem',
      zIndex: 1000,
      minWidth: '280px',
      border: '2px solid #e2e8f0'
    }}>
      <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem'}}>
        <Music size={20} />
        <span style={{fontWeight: 600}}>Background Music</span>
        <button
          onClick={togglePlayPause}
          style={{
            background: isPlaying ? '#ef4444' : '#22c55e',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '30px',
            height: '30px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            marginLeft: 'auto'
          }}
        >
          {isPlaying ? <Pause size={14} /> : <Play size={14} />}
        </button>
      </div>

      {currentSong && (
        <div style={{
          background: '#f0f9ff',
          padding: '0.5rem',
          borderRadius: '6px',
          marginBottom: '1rem',
          fontSize: '0.875rem',
          color: '#1e40af'
        }}>
          🎵 Playing: {currentSong.name}
        </div>
      )}

      <div style={{marginBottom: '1rem'}}>
        <label style={{fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem', display: 'block'}}>
          Choose Music:
        </label>
        <select
          onChange={(e) => {
            const song = musicOptions.find(s => s.id === e.target.value);
            if (song) playMusic(song);
          }}
          value={currentSong?.id || ''}
          style={{
            width: '100%',
            padding: '0.5rem',
            borderRadius: '6px',
            border: '1px solid #e2e8f0',
            fontSize: '0.875rem'
          }}
        >
          <option value="">Select Music</option>
          {musicOptions.map(song => (
            <option key={song.id} value={song.id}>
              {song.name}
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={stopMusic}
        disabled={!isPlaying}
        style={{
          width: '100%',
          padding: '0.5rem',
          background: isPlaying ? '#ef4444' : '#e2e8f0',
          color: isPlaying ? 'white' : '#94a3b8',
          border: 'none',
          borderRadius: '6px',
          cursor: isPlaying ? 'pointer' : 'not-allowed',
          fontSize: '0.875rem',
          fontWeight: 600
        }}
      >
        🔇 Stop Music
      </button>
    </div>
  );
}