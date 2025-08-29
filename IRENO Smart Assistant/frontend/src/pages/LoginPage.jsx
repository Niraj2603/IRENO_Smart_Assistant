import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import styles from './LoginPage.module.css';

const LoginPage = ({ onLogin }) => {
  const { state } = useApp();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    userRole: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate login process
    setTimeout(() => {
      const selectedRole = state.userRoles.find(role => role.id === formData.userRole);
      const user = {
        username: formData.username,
        role: selectedRole,
        avatar: formData.username.charAt(0).toUpperCase()
      };
      
      onLogin(user);
      setIsLoading(false);
    }, 1000);
  };

  const isFormValid = formData.username && formData.password && formData.userRole;

  return (
    <div className={styles.pageContainer}>
      <div className={styles.loginContainer}>
        <div className={styles.loginLeft}>
          <div className={styles.loginBranding}>
            <div className={styles.logo}>
              <div className={styles.logoIcon}>⚡</div>
              <h1>IRENO</h1>
            </div>
            <h2>Smart Assistant</h2>
            <p>ChatGPT-Style AI for Electric Utilities</p>
            <div className={styles.utilityBackground}>
              <div className={styles.gridLines}></div>
              <div className={styles.powerIndicators}>
                <div className={`${styles.indicator} ${styles.active}`}></div>
                <div className={`${styles.indicator} ${styles.active}`}></div>
                <div className={`${styles.indicator} ${styles.warning}`}></div>
              </div>
            </div>
          </div>
        </div>
        
        <div className={styles.loginRight}>
          <div className={styles.loginFormContainer}>
            <h3>Welcome Back</h3>
            <p>Sign in to access your AI-powered utility assistant</p>
            
            <form onSubmit={handleSubmit} className={styles.loginForm}>
              <div className="form-group">
                <label htmlFor="username" className="form-label">Username</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  className="form-control"
                  required
                  placeholder="Enter your username"
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="password" className="form-label">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-control"
                  required
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="userRole" className="form-label">Role</label>
                <select
                  id="userRole"
                  name="userRole"
                  className="form-control"
                  required
                  value={formData.userRole}
                  onChange={handleInputChange}
                >
                  <option value="">Select your role</option>
                  {state.userRoles.map(role => (
                    <option key={role.id} value={role.id}>
                      {role.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <button
                type="submit"
                className="btn btn--primary btn--full-width"
                disabled={!isFormValid || isLoading}
              >
                {isLoading ? 'Signing In...' : 'Sign In'}
              </button>
              
              <div className={styles.loginFooter}>
                <a href="#" className={styles.forgotPassword}>Forgot password?</a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
