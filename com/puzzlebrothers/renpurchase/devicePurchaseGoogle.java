/**
 * Google Play v3 in-app purchase implementation
 *
 * (c) 2013 Emmanuel Marty, marty.emmanuel@gmail.com
 */

package com.puzzlebrothers.renpurchase;

import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.os.Looper;
import com.puzzlebrothers.renpurchase.util.IabHelper;
import com.puzzlebrothers.renpurchase.util.IabResult;
import com.puzzlebrothers.renpurchase.util.Inventory;
import com.puzzlebrothers.renpurchase.util.Purchase;

/**
 * In-app purchase class
 */

public class devicePurchaseGoogle {
   /**
    * Method called on activity creation
    *
    * \param activity game activity
    */
   static public void create (Activity activity) {
      m_singleton = new devicePurchaseGoogle (activity);
   }
   
   /**
    * Method called on activity destruction
    */
   static public void destroy () {
      if (m_singleton != null) {
         m_singleton.cleanup ();
         m_singleton = null;
      }
   }
   
   /**
    * Method called on activity start
    *
    * \param activity game activity
    */
   static public void start (Activity activity) {
      m_activity = activity;
   }
   
   /**
    * Method called on activity stop
    */
   static public void stop () {
      m_activity = null;
   }

   /**
    * Method called when an activity result is received
    *
    * \param requestCode request code
    * \param resultCode result code
    * \param data intent
    * \return true if handled by in-app purchase, false if it must be forwarded to the game activity's superclass
    */
   static public boolean onActivityResult (int requestCode, int resultCode, Intent data) {
      if (m_iabHelper != null)
         return m_iabHelper.handleActivityResult (requestCode, resultCode, data);
      else
         return false;
   }
   
   /**
    * Constructor
    *
    * \param activity game activity
    */
   
   public devicePurchaseGoogle (Activity activity) {
      int nResult;
      
      m_activity = activity;
      m_iabHelper = new IabHelper (m_activity, developerKey.m_base64EncodedPublicKey);
      if (m_iabHelper != null) {
         /*m_iabHelper.enableDebugLogging (true);*/
         m_iabHelper.startSetup (new IabHelper.OnIabSetupFinishedListener () {
            public void onIabSetupFinished (IabResult result) {
               if (result.isSuccess ()) {
                  Log.v ("renpurchase", "Google in-app billing initialized successfully");
                  m_iabAvailable = true;
               }
               else {
                  Log.v ("renpurchase", "Error initializing Google in-app billing");
                  m_iabAvailable = false;
               }
            }
         });
      }
   }
   
   /**
    * Clean resources used by in-app billing
    */
   
   public void cleanup () {
      if (m_iabHelper != null) {
         m_iabHelper.dispose ();
         m_iabHelper = null;
      }
   }

   /**
    * Check if in-app purchases are available on the device
    *
    * \return "1" if available, "0" if not
    */
   static public Integer isPurchasingAvailable() {
      return m_iabAvailable ? ((Integer) 1) : ((Integer) 0);
   }
   
   /**
    * Start the purchase process. Called by the game
    *
    * \param sProductId SKU
    */
   static public void beginPurchase (String sProductId) {
      if (m_iabAvailable && m_activity != null && m_iabHelper != null) {
         m_sProductSku = sProductId;
         m_activity.runOnUiThread (new Runnable () {
            public void run() {
               /* Begin purchase */
               Log.v ("renpurchase", "begin purchase of '" + m_sProductSku + "'");
               m_iabHelper.launchPurchaseFlow (m_activity, m_sProductSku, 10001, m_onPurchaseFinishedListener, "");
            }
         });
      }
      else {
         /** In-app billing not available or initialized, cancel the request */
         Log.v ("renpurchase", "in-app billing not available, cancel purchase request");
         setPurchaseResult (2);
      }
   }
   
   /**
    * Restore existing purchases. Called by the game
    */
   static public void restorePurchases() {
      if (m_iabAvailable && m_activity != null && m_iabHelper != null) {
         Log.v ("renpurchase", "begin restoring purchases");
         if (m_activity != null) m_activity.runOnUiThread (new Runnable () {
            public void run() {
               m_iabHelper.queryInventoryAsync (m_gotInventoryListener);
            }
         });
      }
   }
   
   /**
    * Start the purchase process. Called by the game
    *
    * \param sProductId SKU
    */
   static public void consumePurchase (String sProductId) {
      final String sFinalProductId = sProductId;
      
      if (m_iabAvailable && m_activity != null && m_iabHelper != null) {
         Thread thread = new Thread() {
            @Override
            public void run() {
               try {
                  Looper.prepare ();
                  
                  Log.v ("renpurchase", "consume purchase for '" + sFinalProductId + "'");
                  
                  Inventory inventory = m_iabHelper.queryInventory (false, null, null);
                  if (inventory.hasPurchase (sFinalProductId)) {
                     Log.v ("renpurchase", "consume: inventory obtained, consuming purchase");
                     m_iabHelper.consumeAsync (inventory.getPurchase (sFinalProductId), m_purchaseConsumedListener);
                  }
               } catch (Exception e) {
                  Log.v ("renpurchase", "consume: exception caught: " + e.toString());
               }
            }
         };
         
         thread.start ();
      }
   }
   
   /**
    * Check purchase result. Called by the game
    *
    * \return result
    */
   static public synchronized int checkPurchaseResult () {
      int result = m_purchaseResult;
      
      m_purchaseResult = 0;
      return result;
   }
   
   /**
    * Check if a particular SKU is owned. Called by the game
    *
    * \param sProductId ID of product to check
    *
    * \return 1 if owned, 0 if not
    */
   static public synchronized int isPurchaseOwned (String sProductId) {
      if (m_ownedSkus.contains (sProductId))
         return 1;
      else
         return 0;
   }
   
   /**
    * Set new developer key
    *
    * \param sNewKey key
    */
   static public void setKey (String sNewKey) {
      developerKey.m_base64EncodedPublicKey = sNewKey;
   }
   
   /**
    * Unlock specified achievement
    *
    * \param sAchievementID achievement ID
    */
   static public void unlockAchievement (String sAchievementID) {
   }
   
   /**
    * Set purchase result - internal
    *
    * \param nResult new result
    *
    * \private
    */
   static private synchronized void setPurchaseResult (int nResult) {
      m_purchaseResult = nResult;
   }
   
   /**
    * Add owned product to the list - internal
    *
    * \param sProductId product
    *
    * \private
    */
   static private synchronized void addOwnedProduct (String sProductId) {
      m_ownedSkus.add (sProductId);
   }
   
   /** Listener for in-app purchase results */
   static IabHelper.OnIabPurchaseFinishedListener m_onPurchaseFinishedListener  = new IabHelper.OnIabPurchaseFinishedListener () {
      public void onIabPurchaseFinished(IabResult result, Purchase purchase) {
         Log.v ("renpurchase", "Purchase result: " + result + ", purchase: " + purchase);
         if (result.isFailure ()) {
            if (result.getResponse() == IabHelper.BILLING_RESPONSE_RESULT_ITEM_ALREADY_OWNED) {
               /* Already owned */
               Log.v ("renpurchase", "product '" + m_sProductSku + "' already owned, notifying purchase to game");
               if (m_activity != null) m_activity.runOnUiThread (new Runnable () {
                  public void run() {
                     setPurchaseResult (1);
                     addOwnedProduct (m_sProductSku);
                  }
               });
            }
            else {
               /* Purchase failed */
               Log.v ("renpurchase", "purchasing failure");
               if (m_activity != null) m_activity.runOnUiThread (new Runnable () {
                  public void run() {
                     setPurchaseResult (2);
                  }
               });
            }
         }
         else {
            /* Purchase succeeded */
            if (purchase.getSku().equals (m_sProductSku)) {
               Log.v ("renpurchase", "purchasing succeeded for " + m_sProductSku);
               if (m_activity != null) m_activity.runOnUiThread (new Runnable () {
                  public void run() {
                     setPurchaseResult (1);
                     addOwnedProduct (m_sProductSku);
                  }
               });
            }
            else {
               Log.v ("renpurchase", "purchased unknown product " + purchase.getSku());
               if (m_activity != null) m_activity.runOnUiThread (new Runnable () {
                  public void run() {
                     setPurchaseResult (2);
                  }
               });
            }
         }
      }
   };

   /** Listener for querying the inventory and restoring existing purchases */
   static IabHelper.QueryInventoryFinishedListener m_gotInventoryListener = new IabHelper.QueryInventoryFinishedListener () {
      public void onQueryInventoryFinished (IabResult result, Inventory inventory) {
        Log.v ("renpurchase", "onQueryInventoryFinished");
        setPurchaseResult (2);
        if (result.isFailure ()) {
           Log.v ("renpurchase", "querying the in-app purchases inventory failed");
        }
        else {
           List<Purchase> purchases = inventory.getAllPurchases();

           if (!purchases.isEmpty()) {
              Log.v ("renpurchase", "product already purchased, notifying game");
              setPurchaseResult (1);

              for (Purchase item : purchases) {
                 addOwnedProduct (item.getSku());
              }
           }
           else {
              Log.v ("renpurchase", "inventory retrieved and does not contain product '" + m_sProductSku + "'");
           }
        }
      }
   };

   /** Listener for consuming purchases */
   static IabHelper.OnConsumeFinishedListener m_purchaseConsumedListener = new IabHelper.OnConsumeFinishedListener () {
      public void onConsumeFinished(Purchase purchase, IabResult result) {
         Log.v ("renpurchase", "onConsumeFinished");
      }
   };

   /** Instance of devicePurchaseGoogle */
   static private devicePurchaseGoogle m_singleton = null;

   /** true if in-app billing v3 is available on the device */
   static private volatile boolean m_iabAvailable = false;

   /** Game activity */
   static private Activity m_activity = null;

   /** Instance of in-app billing helper */
   static private IabHelper m_iabHelper = null;

   /** SKU to purchase as defined on the google play developer portal */
   static private String m_sProductSku = "";

   /** Array of owned SKUs */
   static private ArrayList<String> m_ownedSkus = new ArrayList<String>();

   /** Result of the current purchase */
   static private int m_purchaseResult = 0;
}
