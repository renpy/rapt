/**
 * Amazon in-app purchase
 *
 * (c) 2013 Emmanuel Marty, marty.emmanuel@gmail.com
 */

package com.puzzlebrothers.renpurchase;

import java.util.HashSet;
import java.util.Set;
import java.util.EnumSet;
import java.util.ArrayList;
import android.app.Activity;
import android.util.Log;
import android.content.Intent;

import com.amazon.inapp.purchasing.BasePurchasingObserver;
import com.amazon.inapp.purchasing.ItemDataResponse;
import com.amazon.inapp.purchasing.ItemDataResponse.ItemDataRequestStatus;
import com.amazon.inapp.purchasing.PurchaseResponse;
import com.amazon.inapp.purchasing.PurchaseResponse.PurchaseRequestStatus;
import com.amazon.inapp.purchasing.PurchasingManager;
import com.amazon.inapp.purchasing.PurchaseUpdatesResponse;
import com.amazon.inapp.purchasing.Offset;
import com.amazon.inapp.purchasing.Receipt;

/**
 * In-app purchase class
 */

public class devicePurchaseAmazon {
   /**
    * Method called on activity creation
    *
    * \param activity game activity
    */
   static public void create (Activity activity) {
   }

   /**
    * Method called on activity destruction
    */
   static public void destroy () {
   }

   /**
    * Method called on activity start
    *
    * \param view kanji game view
    */
   static public void start (Activity activity) {
      m_activity = activity;
      m_observer = new MyObserver ();
      PurchasingManager.registerObserver (m_observer);
   }

   /**
    * Method called on activity stop
    */
   static public void stop () {
      if (m_observer != null) {
         m_observer = null;
      }
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
      return false;
   }

   /**
    * Start the purchase process. Called by the game
    */
   static public void beginPurchase (String sProductId) {
      setPurchaseResult (0);
      m_sProductSku = sProductId;
      Set<String> skus = new HashSet<String> ();
      skus.add (m_sProductSku);
      Log.v ("renpurchase", "begin item data request for " + m_sProductSku);
      PurchasingManager.initiateItemDataRequest (skus);
   }

   /**
    * Restore existing purchases. Called by the game
    */
   static public void restorePurchases() {
      setPurchaseResult (0);
      Log.v ("renpurchase", "restore purchases");
      PurchasingManager.initiatePurchaseUpdatesRequest(Offset.BEGINNING);
   }

   /**
    * Start the purchase process. Called by the game
    *
    * \param sProductId SKU
    */
   static public void consumePurchase (String sProductId) {
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

   /** Purchase observer */

   static private class MyObserver extends BasePurchasingObserver {
      /** Constructor */
      public MyObserver() {
         super (devicePurchaseAmazon.m_activity);
      }

      /** Respond to product data requests */
      @Override
      public void onItemDataResponse (ItemDataResponse itemDataResponse) {
         if (itemDataResponse.getItemDataRequestStatus() == ItemDataRequestStatus.SUCCESSFUL) {
            /* Succesfully got product info: initiate purchase */
            String requestId = PurchasingManager.initiatePurchaseRequest (m_sProductSku);
            Log.v ("renpurchase", "item data request successful, begin purchase for " + m_sProductSku);
         }
         else {
            /* Failed to get info; cancel purchase */
            setPurchaseResult (2);
            Log.v ("renpurchase", "item data request failed, cancel purchase");
            Log.v ("renpurchase", "itemDataResponse.getItemDataRequestStatus() = " + itemDataResponse.getItemDataRequestStatus());
         }
      }

      /** Respond to purchases */
      @Override
      public void onPurchaseResponse (PurchaseResponse purchaseResponse) {
         if (purchaseResponse.getPurchaseRequestStatus() == PurchaseRequestStatus.SUCCESSFUL ||
             purchaseResponse.getPurchaseRequestStatus() == PurchaseRequestStatus.ALREADY_ENTITLED) {
            /* Purchase succeeded */
            setPurchaseResult (1);
            Log.v ("renpurchase", "purchase successful for sku " + m_sProductSku);
            m_ownedSkus.add (m_sProductSku);
         }
         else {
            /* Purchase failed */
            setPurchaseResult (2);
            Log.v ("renpurchase", "purchase failed");
            Log.v ("renpurchase", "purchaseResponse.getPurchaseRequestStatus() = " + purchaseResponse.getPurchaseRequestStatus());
         }
      }

      /** Respond to restores */
      @Override
      public void onPurchaseUpdatesResponse(final PurchaseUpdatesResponse purchaseUpdatesResponse) {
         Log.v("devicePurchaseAmazon", "onPurchaseUpdatesReceived");

         switch (purchaseUpdatesResponse.getPurchaseUpdatesRequestStatus()) {
         case SUCCESSFUL:
            Log.v("devicePurchaseAmazon", "restore successful");
            setPurchaseResult (2);
            for (final Receipt receipt : purchaseUpdatesResponse.getReceipts()) {
               switch (receipt.getItemType()) {
                  case ENTITLED:
                     Log.v ("renpurchase", "product " + receipt.getSku() + " already entitled");
                     setPurchaseResult (1);
                     Log.v ("renpurchase", "purchase restored");
                     addOwnedProduct (receipt.getSku());
                     break;

                  default:
                     break;
               }
            }
            break;

         default:
            Log.v("devicePurchaseAmazon", "restore failed");
            setPurchaseResult (2);
            break;
         }
      }
   }

   /** SKU to purchase as defined on the amazon developer portal */
   static private String m_sProductSku = "";

   /** Array of owned SKUs */
   static private ArrayList<String> m_ownedSkus = new ArrayList<String>();

   /** Game activity */
   static private Activity m_activity = null;

   /** Amazon purchase observer */
   static private MyObserver m_observer = null;

   /** Result of the current purchase */
   static private int m_purchaseResult = 0;
}
