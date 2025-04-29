import React, { useEffect, useState } from 'react';

function App() {
  const [userID, setUserID] = useState('');
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState('');
  const [editBlocks, setEditBlocks] = useState([{ id: 1, code: '' }]);

  // 產生UserID
  const generateUserID = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
      result = result + chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

  // 初始化全域變數
  const handleInitializeGlobalVariables = async (newUserID) => {
    try {
      const response = await fetch('http://localhost:8000/initialize-global-variables', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userID: newUserID }),
      });

      if (!response.ok) {
        throw new Error('Server error');
      }
    } catch (err) {
      alert(err.message);
    }
  };

  // 執行程式碼
  const handleExecute = async (code) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userID, code }),
      });

      if (!response.ok) {
        throw new Error('Execution failed');
      }

      const result = await response.json();
      if (result.result) {
        setOutput(result.result);
      } else {
        setOutput('No output returned');
      }
    } catch (err) {
      setOutput(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 載入網頁時初始化
  useEffect(() => {
    const newUserID = generateUserID();
    setUserID(newUserID);
    handleInitializeGlobalVariables(newUserID);
  }, []);

  // 新增Edit Block
  const addEditBlock = () => {
    setEditBlocks((previousEditBlocks) => [
      ...previousEditBlocks,
      { id: previousEditBlocks.length + 1, code: '' }
    ]);
  };

  // 更新Code
  const handleCodeChange = (id, event) => {
    const newEditBlocks = editBlocks.map((editBlock) =>
      editBlock.id === id ? { ...editBlock, code: event.target.value } : editBlock
    );
    setEditBlocks(newEditBlocks);
  };

  return (
    <>
      <nav className="navbar is-warning" role="navigation" aria-label="main navigation" style={{ position: 'fixed', top: 0, left: 0, width: '100%', zIndex: 999 }}>
        <div className="navbar-brand">
          <a className="navbar-item" href="/">
            <span className="icon">
              <i className="fa-solid fa-code"></i>
            </span>
            <strong>Python Notebook</strong>
          </a>
        </div>
        <div className="navbar-end">
          <button
            className="navbar-item button is-warning"
            onClick={ () => window.location.reload() }
          >
            Initialization
          </button>
          <button
            className="navbar-item button is-warning"
            onClick={ addEditBlock }
          >
            Add Edit
          </button>
        </div>
      </nav>
      <div style={{ paddingTop: '70px' }}>
        { editBlocks.map((editBlock) => (
          <section key={ editBlock.id } className="section is-flex is-justify-content-center is-align-items-center" style={{ height: 'auto' }}>
            <div className="box" style={{ width: '80%', maxWidth: '900px' }}>
              <h1>{`NO. ${editBlock.id} Edit Block`}</h1>
              <div className="columns is-vcentered">
                <div className="column is-narrow">
                  <div className="buttons is-flex is-flex-direction-column is-align-items-stretch">
                    <button
                      className="button is-success mb-2"
                      onClick={() => handleExecute(editBlock.code)}
                      disabled={loading}
                    >
                      <span className="icon">
                        <i className="fas fa-play"></i>
                      </span>
                      <span>{loading ? 'Running...' : 'Run'}</span>
                    </button>
                  </div>
                </div>

                <div className="column">
                  <textarea
                    className="textarea"
                    rows="8"
                    placeholder="Enter your code..."
                    value={editBlock.code}
                    onChange={(e) => handleCodeChange(editBlock.id, e)}
                  />
                  <pre className="mt-4">{ output }</pre>
                </div>
              </div>
            </div>
          </section>
        ))}
      </div>
    </>
  );
}

export default App;
