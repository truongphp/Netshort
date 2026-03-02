/**
 * Clean Premium Script - Tối ưu hóa cho RevenueCat
 * Chức năng: Mở khóa Locket Gold và các app tương tự
 */

let obj = JSON.parse($response.body);
const ua = $request.headers['User-Agent'] || $request.headers['user-agent'];

// Cấu hình dữ liệu Premium chuẩn
const subscriptionData = {
  "is_sandbox": false,
  "ownership_type": "PURCHASED",
  "billing_issues_detected_at": null,
  "period_type": "normal",
  "expires_date": "2099-12-31T23:59:59Z",
  "purchase_date": "2026-02-03T00:00:00Z",
  "store": "app_store"
};

const entitlementData = {
  "grace_period_expires_date": null,
  "purchase_date": "2026-02-03T00:00:00Z",
  "product_identifier": "com.premium.yearly",
  "expires_date": "2099-12-31T23:59:59Z"
};

// Định nghĩa mapping cho các ứng dụng
const appMapping = {
  'Locket': { entitlement: 'Gold', product: 'com.locket.gold.yearly' },
  '%E8%BD%A6%E7%A5%A8%E7%A5%A8': { entitlement: 'vip', product: 'vip+watch_vip' }
};

// Tìm ứng dụng khớp với User-Agent
const activeApp = Object.keys(appMapping).find(key => ua.includes(key));

if (activeApp) {
  const { entitlement, product } = appMapping[activeApp];
  
  // Gán giá trị vào đúng cấu trúc RevenueCat
  entitlementData.product_identifier = product;
  obj.subscriber.subscriptions[product] = subscriptionData;
  obj.subscriber.entitlements[entitlement] = entitlementData;
} else {
  // Cấu hình mặc định nếu không khớp app nào cụ thể (thường là gói Pro)
  obj.subscriber.subscriptions["com.premium.yearly"] = subscriptionData;
  obj.subscriber.entitlements["pro"] = entitlementData;
}

// Trả về kết quả sạch
$done({ body: JSON.stringify(obj) });
