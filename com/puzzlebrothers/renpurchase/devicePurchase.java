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
   static public void create (Activity activity) {
      try {
         ApplicationInfo appInfo = activity.getPackageManager().getApplicationInfo (activity.getPackageName(), PackageManager.GET_META_DATA);
         Object value = appInfo.metaData.get ("renpy-store");
         String strValue = value.toString ();
         
         if (strValue != null) {
            m_store = strValue;
         }
      } catch (Exception e) {
      }
      
      Log.v ("renpurchase", "devicePurchase.create with store: " + m_store);
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.create (activity);
      else
         devicePurchaseAmazon.create (activity);
   }
   
   /**
    * Method called on activity destruction
    */
   static public void destroy () {
      Log.v ("renpurchase", "devicePurchase.destroy");
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.destroy ();
      else
         devicePurchaseAmazon.destroy ();
   }
   
   /**
    * Method called on activity start
    *
    * \param view kanji game view
    */
   static public void start (Activity activity) {
      Log.v ("renpurchase", "devicePurchase.start");
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.start (activity);
      else
         devicePurchaseAmazon.start (activity);
   }
   
   /**
    * Method called on activity stop
    */
   static public void stop () {
      Log.v ("renpurchase", "devicePurchase.stop");
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.stop ();
      else
         devicePurchaseAmazon.stop ();
   }
   
   /**
    * Method called when an activity result is received
    *
    * \param requestCode request code
    * \param resultCode result code
    * \param data intent
    *
    * \return true if handled by in-app purchase, false if it must be forwarded to the game activity's superclass
    */
   static public boolean onActivityResult (int requestCode, int resultCode, Intent data) {
      if (m_store.equalsIgnoreCase ("google"))
         return devicePurchaseGoogle.onActivityResult (requestCode, resultCode, data);
      else
         return devicePurchaseAmazon.onActivityResult (requestCode, resultCode, data);
   }
   
   /**
    * Start the purchase process. Called by the game
    */
   static public void beginPurchase (String sProductId) {
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.beginPurchase (sProductId);
      else
         devicePurchaseAmazon.beginPurchase (sProductId);
   }
   
   /**
    * Restore existing purchases. Called by the game
    */
   static public void restorePurchases() {
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.restorePurchases ();
      else
         devicePurchaseAmazon.restorePurchases ();
   }
   
   /**
    * Start the purchase process. Called by the game
    *
    * \param sProductId SKU
    */
   static public void consumePurchase (String sProductId) {
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.consumePurchase (sProductId);
      else
         devicePurchaseAmazon.consumePurchase (sProductId);
   }
   
   /**
    * Check purchase result. Called by the game
    *
    * \return result
    */
   static public synchronized int checkPurchaseResult () {
      if (m_store.equalsIgnoreCase ("google"))
         return devicePurchaseGoogle.checkPurchaseResult ();
      else
         return devicePurchaseAmazon.checkPurchaseResult ();
   }
   
   /**
    * Check if a particular SKU is owned. Called by the game
    *
    * \param sProductId ID of product to check
    *
    * \return 1 if owned, 0 if not
    */
   static public synchronized int isPurchaseOwned (String sProductId) {
      if (m_store.equalsIgnoreCase ("google"))
         return devicePurchaseGoogle.isPurchaseOwned (sProductId);
      else
         return devicePurchaseAmazon.isPurchaseOwned (sProductId);
   }
   
   /**
    * Set new developer key
    *
    * \param sNewKey key
    */
   static public void setKey (String sNewKey) {
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.setKey (sNewKey);
      else
         devicePurchaseAmazon.setKey (sNewKey);
   }
   
   /**
    * Unlock specified achievement
    *
    * \param sAchievementID achievement ID
    */
   static public void unlockAchievement (String sAchievementID) {
      if (m_store.equalsIgnoreCase ("google"))
         devicePurchaseGoogle.unlockAchievement (sAchievementID);
      else
         devicePurchaseAmazon.unlockAchievement (sAchievementID);
   }
   
   /** SKU to purchase as defined on the amazon developer portal */
   static private String m_store = "google";
}
