import CryptoJS from 'crypto-js';

export const encryptApiKey = (apiKey: string, salt: string) => {
  return CryptoJS.AES.encrypt(apiKey, salt).toString();
};

export const generateDynamicSalt = () => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};
