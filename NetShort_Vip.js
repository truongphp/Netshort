/*
 * Script bẻ khóa NetShort & RevenueCat Apps
 * Hạn dùng: Vĩnh viễn (2099)
 */

var obj = JSON.parse($response.body);
var ua = $request.headers["User-Agent"] || $request.headers["user-agent"];

// Cấu hình thông tin VIP giả lập
var vipInfo = {
  "is_sandbox": false,
  "ownership_type": "PURCHASED",
  "billing_issues_detected_at": null,
  "period_type": "normal",
  "expires_date": "2099-12-31T23:59:59Z",
  "original_purchase_date": "2024-01-01T00:00:00Z",
  "purchase_date": "2024-01-01T00:00:00Z",
  "store": "app_store"
};

var entitlementInfo = {
  "grace_period_expires_date": null,
  "purchase_date": "2024-01-01T00:00:00Z",
  "product_identifier": "netshort_premium_yearly",
  "expires_date": "2099-12-31T23:59:59Z"
};

// Danh sách các ID định danh của NetShort và các app tương tự
const sub_id = "netshort_premium_yearly"; // ID mặc định
const ent_id = "premium"; // Quyền hạn mặc định

if (obj.subscriber) {
  // 1. Gán gói đăng ký (Subscriptions)
  obj.subscriber.subscriptions[sub_id] = vipInfo;
  
  // 2. Gán quyền hạn thành viên (Entitlements)
  // Thử gán cho các tag phổ biến của app phim ngắn
  obj.subscriber.entitlements["premium"] = entitlementInfo;
  obj.subscriber.entitlements["vip"] = entitlementInfo;
  obj.subscriber.entitlements["pro"] = entitlementInfo;
  obj.subscriber.entitlements["Gold"] = entitlementInfo; // Dùng cho Locket luôn
}

obj.Attention = "Đã bẻ khóa NetShort VIP bởi Gemini - Chúc mừng vọc sĩ!";

$done({ body: JSON.stringify(obj) });
