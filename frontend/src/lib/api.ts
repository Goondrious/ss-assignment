import { API_URL } from "./constants";
import { NewCompressionInput } from "./types";

export const authenticatedFetch = (
  url: string,
  token: string,
  params: any = {}
) => {
  return fetch(url, {
    ...params,
    headers: { ...(params.headers || {}), authorization: `Bearer ${token}` },
  });
};

export const runStandardizedFetch = async (
  fetchFn: () => Promise<Response>
) => {
  try {
    const res = await fetchFn();

    if (!res.ok) {
      const error = await res
        .json()
        .then((o) => o.detail)
        .catch((o) => o.text);

      return { error };
    }

    const data = await res.json();
    return { data };
  } catch (e: any) {
    console.error("Error fetching data", e.message);
    return { error: e.message };
  }
};

export const fetchUserFromAPI = async (token: string) => {
  const userFetch = () => authenticatedFetch(`${API_URL}/user/me`, token);
  return runStandardizedFetch(userFetch);
};

export const fetchTokenFromAPI = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const tokenFetch = () =>
    fetch(`${API_URL}/token`, {
      method: "POST",
      body: formData,
    });

  return runStandardizedFetch(tokenFetch);
};

export const fetchImagesFromAPI = async (token: string) => {
  const imagesFetch = () => authenticatedFetch(`${API_URL}/images`, token);
  return runStandardizedFetch(imagesFetch);
};

export const uploadImageToAPI = async (
  file: File,
  fileName: string,
  token: string
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_name", fileName);

  const uploadImageFetch = () =>
    authenticatedFetch(`${API_URL}/image`, token, {
      method: "PUT",
      body: formData,
    });

  return runStandardizedFetch(uploadImageFetch);
};

export const fetchImageFromAPI = async (imageId: string, token: string) => {
  const imageFetch = () =>
    authenticatedFetch(`${API_URL}/image/${imageId}`, token);
  return runStandardizedFetch(imageFetch);
};

export const deleteImageFromAPI = async (imageId: string, token: string) => {
  const deleteImageFetch = () =>
    authenticatedFetch(`${API_URL}/image/${imageId}`, token, {
      method: "DELETE",
    });

  return runStandardizedFetch(deleteImageFetch);
};

export const fetchImageCompressionsFromAPI = async (
  imageId: string,
  token: string
) => {
  const imageCompressionsFetch = () =>
    authenticatedFetch(`${API_URL}/image/${imageId}/image-compressions`, token);
  return runStandardizedFetch(imageCompressionsFetch);
};

export const addCompressionToAPI = async (
  { imageId, quality, resizeWidth }: NewCompressionInput,
  token: string
) => {
  const formData = new FormData();
  formData.append("image_id", imageId);
  formData.append("quality", `${quality}`);
  formData.append("resize_width", `${resizeWidth}`);

  const addCompressionFetch = () =>
    authenticatedFetch(`${API_URL}/image/${imageId}/image-compression`, token, {
      method: "PUT",
      body: formData,
    });

  return runStandardizedFetch(addCompressionFetch);
};

export const deleteImageCompressionFromAPI = async (
  imageId: string,
  compressionId: string,
  token: string
) => {
  const deleteImageCompressionFetch = () =>
    authenticatedFetch(
      `${API_URL}/image/${imageId}/image-compression/${compressionId}`,
      token,
      {
        method: "DELETE",
      }
    );

  return runStandardizedFetch(deleteImageCompressionFetch);
};
