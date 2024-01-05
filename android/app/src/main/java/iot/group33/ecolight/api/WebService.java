package iot.group33.ecolight.api;

import iot.group33.ecolight.Info;
import retrofit2.Call;
import retrofit2.http.GET;

public interface WebService {
    @GET("/info")
    Call<Info> getInfo();
}
