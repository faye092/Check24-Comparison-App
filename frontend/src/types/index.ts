// src/types/index.ts

// 比赛相关的类型定义
export interface Game {
    id: number;
    team_home: string;
    team_away: string;
    starts_at: string;
    tournament_name: string;
  }
  
  // 流媒体套餐类型
  export interface StreamingPackage {
    id: number;
    name: string;
    monthly_price_cents: number;
    monthly_price_yearly_subscription_in_cents: number;
    live: boolean;
    highlights: boolean;
  }
  
  // 通用的 API 响应类型
  export interface FetchResponse<T> {
    data: T;
  }
  