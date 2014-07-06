/**
 * In-app purchase store selector
 *
 * (c) 2013 Emmanuel Marty, marty.emmanuel@gmail.com
 */

package com.puzzlebrothers.renpurchase;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.app.Activity;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;

/**
 * In-app purchase selector class
 */

public class devicePurchase {
	/**
	 * Method called on activity creation
	 *
	 * \param activity game activity
	 */

	static final int NONE = 0;
	static final int PLAY = 1;
	static final int AMAZON = 2;

	static public void create(Activity activity) {

		String store = org.renpy.android.Constants.store;

		if (store.equals("play")) {
			m_store = PLAY;
			devicePurchaseGoogle.create(activity);
		} else if (store.equals("amazon")) {
			m_store = AMAZON;
			devicePurchaseAmazon.create(activity);
		} else {
			m_store = NONE;
		}
	}

	/**
	 * Method called on activity destruction
	 */
	static public void destroy() {
		Log.v("renpurchase", "devicePurchase.destroy");

		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.destroy();
			break;
		case AMAZON:
			devicePurchaseAmazon.destroy();
			break;
		}
	}

	/**
	 * Method called on activity start
	 *
	 * \param view kanji game view
	 */
	static public void start(Activity activity) {
		Log.v("renpurchase", "devicePurchase.start");

		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.start(activity);
			break;
		case AMAZON:
			devicePurchaseAmazon.start(activity);
			break;
		}
	}

	/**
	 * Method called on activity stop
	 */
	static public void stop() {
		Log.v("renpurchase", "devicePurchase.stop");
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.stop();
			break;
		case AMAZON:
			devicePurchaseAmazon.stop();
			break;
		}
	}

	/**
	 * Method called when an activity result is received
	 *
	 * \param requestCode request code \param resultCode result code \param data
	 * intent
	 *
	 * \return true if handled by in-app purchase, false if it must be forwarded
	 * to the game activity's superclass
	 */
	static public boolean onActivityResult(int requestCode, int resultCode,
			Intent data) {
		switch(m_store) {
		case PLAY:
			return devicePurchaseGoogle.onActivityResult(requestCode,
					resultCode, data);
		case AMAZON:
			return devicePurchaseAmazon.onActivityResult(requestCode,
					resultCode, data);
		}

		return false;
	}

	/**
	 * Start the purchase process. Called by the game
	 */
	static public void beginPurchase(String sProductId) {
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.beginPurchase(sProductId);
			break;
		case AMAZON:
			devicePurchaseAmazon.beginPurchase(sProductId);
			break;
		}
	}

	/**
	 * Restore existing purchases. Called by the game
	 */
	static public void restorePurchases() {
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.restorePurchases();
			break;
		case AMAZON:
			devicePurchaseAmazon.restorePurchases();
			break;
		}
	}

	/**
	 * Start the purchase process. Called by the game
	 *
	 * \param sProductId SKU
	 */
	static public void consumePurchase(String sProductId) {
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.consumePurchase(sProductId);
			break;
		case AMAZON:
			devicePurchaseAmazon.consumePurchase(sProductId);
			break;
		}
	}

	/**
	 * Check purchase result. Called by the game
	 *
	 * \return result
	 */
	static public synchronized int checkPurchaseResult() {
		switch(m_store) {
		case PLAY:
			return devicePurchaseGoogle.checkPurchaseResult();
		case AMAZON:
			return devicePurchaseAmazon.checkPurchaseResult();
		}

		return 2; // Not available.
	}

	/**
	 * Check if a particular SKU is owned. Called by the game
	 *
	 * \param sProductId ID of product to check
	 *
	 * \return 1 if owned, 0 if not
	 */
	static public synchronized int isPurchaseOwned(String sProductId) {
		switch(m_store) {
		case PLAY:
			return devicePurchaseGoogle.isPurchaseOwned(sProductId);
		case AMAZON:
			return devicePurchaseAmazon.isPurchaseOwned(sProductId);
		}

		return 0;
	}

	/**
	 * Set new developer key
	 *
	 * \param sNewKey key
	 */
	static public void setKey(String sNewKey) {
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.setKey(sNewKey);
			break;
		case AMAZON:
			devicePurchaseAmazon.setKey(sNewKey);
			break;
		}
	}

	/**
	 * Unlock specified achievement
	 *
	 * \param sAchievementID achievement ID
	 */
	static public void unlockAchievement(String sAchievementID) {
		switch(m_store) {
		case PLAY:
			devicePurchaseGoogle.unlockAchievement(sAchievementID);
			break;
		case AMAZON:
			devicePurchaseAmazon.unlockAchievement(sAchievementID);
			break;
		}
	}

	/** SKU to purchase as defined on the amazon developer portal */
	static private int m_store = NONE;
}
