package org.renpy.android;

import org.libsdl.app.SDLActivity;

import android.app.Activity;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;

public class PythonSDLActivity extends SDLActivity {

	public native void nativeSetEnv(String variable, String value);
    ResourceManager resourceManager;

    /**
     * This determines if unpacking one the zip files included in
     * the .apk is necessary. If it is, the zip file is unpacked.
     */
    public void unpackData(final String resource, File target) {

    	/**
    	 * Delete main.pyo unconditionally. This fixes a problem where we have
    	 * a main.py newer than main.pyo, but start.c won't run it.
    	 */
    	new File(target, "main.pyo").delete();

        // The version of data in memory and on disk.
        String data_version = resourceManager.getString(resource + "_version");
        String disk_version = null;

        // If no version, no unpacking is necessary.
        if (data_version == null) {
            return;
        }

        // Check the current disk version, if any.
        String filesDir = target.getAbsolutePath();
        String disk_version_fn = filesDir + "/" + resource + ".version";

        try {
            byte buf[] = new byte[64];
            InputStream is = new FileInputStream(disk_version_fn);
            int len = is.read(buf);
            disk_version = new String(buf, 0, len);
            is.close();
        } catch (Exception e) {
            disk_version = "";
        }

        // If the disk data is out of date, extract it and write the
        // version file.
        if (! data_version.equals(disk_version)) {
            Log.v("python", "Extracting " + resource + " assets.");

            // recursiveDelete(target);
            target.mkdirs();

            AssetExtract ae = new AssetExtract(this);
            if (!ae.extractTar(resource + ".mp3", target.getAbsolutePath())) {
                toastError("Could not extract " + resource + " data.");
            }

            try {
                // Write .nomedia.
                new File(target, ".nomedia").createNewFile();

                // Write version file.
                FileOutputStream os = new FileOutputStream(disk_version_fn);
                os.write(data_version.getBytes());
                os.close();
            } catch (Exception e) {
                Log.w("python", e);
            }
        }

    }

    /**
     * Show an error using a toast. (Only makes sense from non-UI
     * threads.)
     */
    public void toastError(final String msg) {

        final Activity thisActivity = this;

        runOnUiThread(new Runnable () {
            public void run() {
                Toast.makeText(thisActivity, msg, Toast.LENGTH_LONG).show();
            }
        });

        // Wait to show the error.
        synchronized (this) {
            try {
                this.wait(1000);
            } catch (InterruptedException e) {
            }
        }
    }


    public void preparePython() {
        Log.v("python", "Starting preparePython.");

        resourceManager = new ResourceManager(this);

        File oldExternalStorage = new File(Environment.getExternalStorageDirectory(), getPackageName());
        File externalStorage = getExternalFilesDir(null);
        File path;

        if (externalStorage == null) {
        	externalStorage = oldExternalStorage;
        }

        if (resourceManager.getString("public_version") != null) {
            path = externalStorage;
        } else {
        	path = getFilesDir();
        }

        unpackData("private", getFilesDir());
        unpackData("public", externalStorage);

    	nativeSetEnv("ANDROID_ARGUMENT", path.getAbsolutePath());
		nativeSetEnv("ANDROID_PRIVATE", getFilesDir().getAbsolutePath());
    	nativeSetEnv("ANDROID_PUBLIC",  externalStorage.getAbsolutePath());
    	nativeSetEnv("ANDROID_OLD_PUBLIC", oldExternalStorage.getAbsolutePath());

    	// Figure out the APK path.
        String apkFilePath;
        ApplicationInfo appInfo;
        PackageManager packMgmr = getApplication().getPackageManager();

        try {
            appInfo = packMgmr.getApplicationInfo(getPackageName(), 0);
            apkFilePath = appInfo.sourceDir;
        } catch (NameNotFoundException e) {
            apkFilePath = "";
        }

    	nativeSetEnv("ANDROID_APK", apkFilePath);

    	String expansionFile = getIntent().getStringExtra("expansionFile");

    	if (expansionFile != null) {
    		nativeSetEnv("ANDROID_EXPANSION", expansionFile);
    	}

    	nativeSetEnv("PYTHONOPTIMIZE", "2");
    	nativeSetEnv("PYTHONHOME", getFilesDir().getAbsolutePath());
    	nativeSetEnv("PYTHONPATH", path.getAbsolutePath() + ":" + getFilesDir().getAbsolutePath() + "/lib");

        Log.v("python", "Finished preparePython.");


    };

}
