package iot.group33.ecolight;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Locale;
import java.util.Objects;

import iot.group33.ecolight.api.WebService;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class LayoutActivity extends AppCompatActivity {

    Button btnCommand;

    Button btnUpdate;

    TextView tvCommandResult;

    TextView tvIndoorTemp;

    TextView tvIndoorHumidity;

    private static final int REQUEST_CODE_SPEECH_INPUT = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout);

        tvCommandResult = (TextView) findViewById(R.id.tvCommandResult) ;
        tvIndoorTemp = (TextView) findViewById(R.id.indoorTempShow);
        tvIndoorHumidity = (TextView) findViewById(R.id.indoorHumiShow);
        btnCommand = (Button) findViewById(R.id.btn_command);
        btnUpdate = (Button) findViewById(R.id.btnUpdateTemp);
        btnCommand.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent
                        = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,
                        Locale.getDefault());
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to text");

                try {
                    startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT);
                }
                catch (Exception e) {
                    Toast
                            .makeText(LayoutActivity.this, " " + e.getMessage(),
                                    Toast.LENGTH_SHORT)
                            .show();
                }
            }
        });

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
}
