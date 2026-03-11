//gloabal way to interact with the backend

const baseURL = "http://localhost:5000/api";
//api is wrapper around the fetch
const api = {

  async request(endpoint, options = {}) {
//ensuring endpoints starts with a slash
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${baseURL.replace(/\/$/, "")}${path}`;

    const token = localStorage.getItem("access_token");

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authentication-Token"] = token;
    }

    const config = {
      ...options,
      headers,
    };

    try {

      const response = await fetch(url, config);
//error handling
      if (response.status === 401) {
        alert("Session expired. Please login again.");
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
        throw new Error("Unauthorized");
      }

      if (!response.ok) {

        let bodyText = null;

        try {
          bodyText = await response.text();
        } catch (e) {}

        let friendlyMessage;
        try {
          const parsed = JSON.parse(bodyText);
          friendlyMessage = parsed.message || parsed.error || parsed.response?.errors?.[0] || bodyText;
        } catch {
          friendlyMessage = bodyText || `HTTP error! status: ${response.status}`;
        }
        const message = friendlyMessage;

        const err = new Error(message);
        err.status = response.status;
        throw err;
      }

      if (response.status === 204) return null;

      const text = await response.text();

      if (!text) return null;

      try {
        return JSON.parse(text);
      } catch {
        return text;
      }

    } catch (error) {
      return Promise.reject(error);
    }

  },

  get(endpoint, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "GET",
    });
  },

  post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  patch(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "DELETE",
    });
  },

};

export default api;
