import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [noCount, setNoCount] = useState(0);
  const [yesClicked, setYesClicked] = useState(false);
  const [shakeClass, setShakeClass] = useState('');
  const [noButtonPos, setNoButtonPos] = useState({ top: 'auto', left: 'auto' });
  const [isCaught, setIsCaught] = useState(false);

  useEffect(() => {
    let intervalId;
    if (noCount === 4 && !isCaught) {
      intervalId = setInterval(() => {
        moveNoButton();
      }, 1500);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [noCount, isCaught]);

  const handleNoClick = () => {
    if (noCount >= 5) return;
    
    setNoCount(prev => prev + 1);
    
    let shakeLevel = '';
    if (noCount === 0) shakeLevel = 'shake-level-1';
    else if (noCount === 1) shakeLevel = 'shake-level-2';
    else if (noCount >= 2) shakeLevel = 'shake-level-3';
    
    setShakeClass(shakeLevel);
    
    setTimeout(() => {
      setShakeClass('');
    }, 600);

    // 3回目をクリックして4回目（逃走）に入る瞬間に座標を初期化
    if (noCount === 3) {
      moveNoButton();
      setIsCaught(false);
    }
  };

  const moveNoButton = () => {
    const x = Math.max(20, Math.random() * (window.innerWidth - 150));
    const y = Math.max(20, Math.random() * (window.innerHeight - 100));
    setNoButtonPos({ top: `${y}px`, left: `${x}px` });
  };

  const handleNoMouseEnter = () => {
    if (noCount === 4) setIsCaught(true);
  };

  const handleNoMouseLeave = () => {
    if (noCount === 4) setIsCaught(false);
  };

  const handleYesClick = () => {
    setYesClicked(true);
    document.body.classList.add('love-mode');
  };

  // Yesボタンの巨大化を少しマイルドにして画面外に押し出さないようにする
  const getYesButtonSize = () => {
    if (noCount === 0) return 1.2;
    if (noCount === 1) return 1.5;
    if (noCount === 2) return 2.0;
    if (noCount === 3) return 2.8;
    return 3.5; 
  };

  const getYesButtonPadding = () => {
    if (noCount === 0) return '12px 30px';
    if (noCount === 1) return '15px 40px';
    if (noCount === 2) return '20px 50px';
    if (noCount === 3) return '30px 60px';
    return '40px 70px';
  };

  // Noボタンは逆に少しずつ小さくする（より押しにくくする）
  const getNoButtonSize = () => {
    if (noCount === 0) return 1.2;
    if (noCount === 1) return 1.0;
    if (noCount === 2) return 0.9;
    if (noCount === 3) return 0.8;
    return 1.2; // 逃げる時は元のサイズに戻す
  };

  const renderNoButton = (isRunaway = false) => (
    <button 
      className={`btn btn-no ${isRunaway ? 'btn-runaway' : ''} ${isCaught ? 'btn-caught' : ''}`}
      style={isRunaway ? {
        top: noButtonPos.top,
        left: noButtonPos.left,
        fontSize: `${getNoButtonSize()}rem`,
        padding: '12px 30px'
      } : {
        fontSize: `${getNoButtonSize()}rem`
      }}
      onClick={handleNoClick}
      onMouseEnter={isRunaway ? handleNoMouseEnter : undefined}
      onMouseLeave={isRunaway ? handleNoMouseLeave : undefined}
    >
      No
    </button>
  );

  return (
    <>
      <div className={`app-container ${shakeClass}`}>
        
        {yesClicked ? (
          <div className="success-screen">
            <h1 className="question-text">知ってた！❤️</h1>
            <img src="/happy_cat.png" alt="Happy Cat" className="cat-image" />
          </div>
        ) : noCount >= 5 ? (
          <div className="sad-screen">
            <h1 className="question-text" style={{color: '#6c757d', fontSize: '1.8rem'}}>どうしてもダメ…？</h1>
            <img src="/sad_cat.png" alt="Sad Cat" className="cat-image" />
          </div>
        ) : (
          <>
            <h1 className="question-text">Do you love me?</h1>
            
            <div className="button-container">
              <button 
                className="btn btn-yes"
                style={{ 
                  fontSize: `${getYesButtonSize()}rem`, 
                  padding: getYesButtonPadding()
                }}
                onClick={handleYesClick}
              >
                Yes
              </button>
              
              {noCount < 4 && renderNoButton(false)}
            </div>
          </>
        )}
      </div>

      {noCount === 4 && !yesClicked && renderNoButton(true)}
    </>
  );
}

export default App;
