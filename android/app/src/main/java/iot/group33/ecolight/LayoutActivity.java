package iot.group33.ecolight;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Objects;

import iot.group33.ecolight.api.WebService;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class LayoutActivity extends AppCompatActivity {

    Button btnRecord;

    Button btnUpdate;

    TextView tvCommandResult;

    TextView tvIndoorTemp;

    TextView tvIndoorHumidity;

    private static final int REQUEST_CODE_SPEECH_INPUT = 1;

    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;

    private Button recordButton = null;
    private MediaRecorder recorder = null;

    private Button   playButton = null;
    private MediaPlayer player = null;
    private String [] permissions = {Manifest.permission.RECORD_AUDIO};
    private static String fileName = null;

    private boolean isRecording = false;

    private boolean isPlaying = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout);

        fileName = getExternalCacheDir().getAbsolutePath();
        fileName += "/audiorecordtest.3gp";

        ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);

        tvCommandResult = (TextView) findViewById(R.id.tvCommandResult) ;
        tvIndoorTemp = (TextView) findViewById(R.id.indoorTempShow);
        tvIndoorHumidity = (TextView) findViewById(R.id.indoorHumiShow);
        btnUpdate = (Button) findViewById(R.id.btnUpdateTemp);
        btnRecord = (Button) findViewById(R.id.btn_record);

        btnUpdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
                StrictMode.setThreadPolicy(policy);
                try {
                    Retrofit retrofit = new Retrofit.Builder()
                            .baseUrl("http://10.0.2.2:5000")
                            .addConverterFactory(GsonConverterFactory.create())
                            .build();

                    WebService service = retrofit.create(WebService.class);
                    Call<Info> infoCall = service.getInfo();
                    Info info = infoCall.execute().body();
                    tvIndoorTemp.setText(String.valueOf(info.temperature));
                    tvIndoorHumidity.setText(String.valueOf(info.humidity));
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        btnRecord.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!isRecording) {
                    btnRecord.setText("Stop command");
                    onRecord(true);
                } else {
                    btnRecord.setText("Start command");
                    onRecord(false);

                    File file = new File(fileName);
                    RequestBody requestFile =
                            RequestBody.create(
                                    MediaType.parse("audio/3gp"),
                                    file
                            );

                    // MultipartBody.Part is used to send also the actual file name
                    MultipartBody.Part body =
                            MultipartBody.Part.createFormData("file", file.getName(), requestFile);

                    // add another part within the multipart request
                    String descriptionString = "hello, this is description speaking";
                    RequestBody description =
                            RequestBody.create(
                                    okhttp3.MultipartBody.FORM, descriptionString);

                    StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
                    StrictMode.setThreadPolicy(policy);
                    try {
                        Retrofit retrofit = new Retrofit.Builder()
                                .baseUrl("http://10.0.2.2:5000")
                                .addConverterFactory(GsonConverterFactory.create())
                                .build();

                        WebService service = retrofit.create(WebService.class);
                        Call<Command> call = service.getVoiceCommand(body);
                        Command response = call.execute().body();
                        String result = response.getResult();

                        if (result.equals("happy") || result.equals("neutral")) {
                            tvCommandResult.setText("Emotion: " + result + ". We will turn on the lights");
                        } else {
                            tvCommandResult.setText("Emotion: " + result + ". We will turn on the lights");
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }



                }
                isRecording = !isRecording;
            }
        });

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQUEST_RECORD_AUDIO_PERMISSION:
                if (grantResults.length > 0) {
                    boolean permissionToRecord = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                    if (permissionToRecord) {
                    } else {
                        Toast.makeText(getApplicationContext(), "Permission Denied", Toast.LENGTH_LONG).show();
                    }
                }
                break;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_SPEECH_INPUT) {
            if (resultCode == RESULT_OK && data != null) {
                ArrayList<String> result = data.getStringArrayListExtra(
                        RecognizerIntent.EXTRA_RESULTS);
                tvCommandResult.setText(
                        Objects.requireNonNull(result).get(0));
            }
        }
    }

    private void onRecord(boolean start) {
        if (start) {
            startRecording();
        } else {
            stopRecording();
        }
    }

    private void onPlay(boolean start) {
        if (start) {
            startPlaying();
        } else {
            stopPlaying();
        }
    }

    private void startPlaying() {
        player = new MediaPlayer();
        try {
            player.setDataSource(fileName);
            player.prepare();
            player.start();
        } catch (IOException e) {
            Log.e("LayoutActivity", "prepare() failed");
        }
    }

    private void stopPlaying() {
        player.release();
        player = null;
    }

    private void startRecording() {
        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setOutputFile(fileName);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            recorder.prepare();
        } catch (IOException e) {
            Log.e("LayoutActivity", "prepare() failed");
        }

        recorder.start();
    }

    private void stopRecording() {
        recorder.stop();
        recorder.release();
        recorder = null;
    }

}
