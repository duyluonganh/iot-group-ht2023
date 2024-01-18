package iot.group33.ecolight.api;

import java.io.File;

import iot.group33.ecolight.Command;
import iot.group33.ecolight.Info;
import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface WebService {
    @GET("/info")
    Call<Info> getInfo();

    @Multipart
    @POST("/voice_command")
    Call<Command> getVoiceCommand(@Part MultipartBody.Part file);
}
