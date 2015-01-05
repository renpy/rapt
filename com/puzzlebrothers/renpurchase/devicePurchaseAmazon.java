/**
 * Amazon in-app purchase
 *
 * (c) 2013 Emmanuel Marty, marty.emmanuel@gmail.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package com.puzzlebrothers.renpurchase;

import java.util.ArrayList;

import com.amazon.device.iap.PurchasingListener;
import com.amazon.device.iap.PurchasingService;
import com.amazon.device.iap.model.ProductDataResponse;
import com.amazon.device.iap.model.PurchaseResponse;
import com.amazon.device.iap.model.PurchaseUpdatesResponse;
import com.amazon.device.iap.model.Receipt;
import com.amazon.device.iap.model.UserDataResponse;

import android.app.Activity;
import android.util.Log;
import android.content.Intent;

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
        listener = new MyPurchasingListener();
        PurchasingService.registerListener(activity.getApplicationContext(), listener);
        Log.i("renpurchase", "Amazon, sandbox = " + PurchasingService.IS_SANDBOX_MODE);
        Log.i("renpurchase", "CONTEXT " + activity.getApplicationContext());
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
    }

    /**
     * Method called on activity stop
     */
    static public void stop () {
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
    static public void beginPurchase(String productId) {
        setPurchaseResult (0);
        Log.v ("renpurchase", "begin purchase of " + productId);
        PurchasingService.purchase(productId);
    }

    /**
     * Restore existing purchases. Called by the game
     */
    static public void restorePurchases() {
        setPurchaseResult (0);
        Log.v ("renpurchase", "restore purchases");
        PurchasingService.getPurchaseUpdates(true);
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
    static private synchronized void addOwnedProduct(String sProductId) {
        m_ownedSkus.add (sProductId);
    }

    /** Array of owned SKUs */
    static private ArrayList<String> m_ownedSkus = new ArrayList<String>();

    /** Result of the current purchase */
    static private int m_purchaseResult = 0;

    static private MyPurchasingListener listener;

    public static class MyPurchasingListener implements PurchasingListener {

        @Override
        public void onUserDataResponse(final UserDataResponse response) {
        }

        @Override
        public void onPurchaseUpdatesResponse(final PurchaseUpdatesResponse response) {
            Log.i("renpurchase", "onPurchaseUpdatesResponse status " + response.getRequestStatus());

            if (response.getRequestStatus() != PurchaseUpdatesResponse.RequestStatus.SUCCESSFUL) {
                setPurchaseResult(2);
            }

            for (Receipt r : response.getReceipts()) {
                if (! r.isCanceled()) {
                    addOwnedProduct(r.getSku());
                }
            }

            if (response.hasMore()) {
                PurchasingService.getPurchaseUpdates(false);
            } else {
                setPurchaseResult(1);
            }

        }

        @Override
        public void onPurchaseResponse(final PurchaseResponse response) {
            if (response.getRequestStatus() != PurchaseResponse.RequestStatus.SUCCESSFUL) {
                Log.i("renpurchase", "onPurchaseResponse status " + response.getRequestStatus());
                setPurchaseResult(2);
            }

            addOwnedProduct(response.getReceipt().getSku());
            setPurchaseResult(1);
        }

        @Override
        public void onProductDataResponse(ProductDataResponse arg0) {
        }
    }


}
